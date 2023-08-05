#!/usr/bin/env python

import torch
import numpy as np
import sys
from wuml.IO import *
from sklearn import linear_model
from torch import nn
from torch.autograd import Variable
from inspect import signature
import torch.nn.functional as F
import torch.nn as nn
import collections

class flexable_Model(torch.nn.Module):
	def __init__(self, dataDim, networkStructure):
		super(flexable_Model, self).__init__()

		self.networkStructure = networkStructure
		inDim = dataDim
		for l, Layer_info in enumerate(networkStructure):
			layer_width, activation_function = Layer_info
			φ = activation_function
			outDim = layer_width

			lr = 'self.l' + str(l) + ' = torch.nn.Linear(' + str(inDim) + ', ' + str(outDim) + ' , bias=True)'
			exec(lr)
			exec('self.l' + str(l) + '.activation = "' + φ + '"')		#softmax, relu, tanh, sigmoid, none
			inDim = outDim

	def forward(self, x):
		self.y0 = x
		for m, layer in enumerate(self.children(),0):
			var = 'self.y' + str(m+1)

			if layer.activation == 'none':
				cmd = 'self.yout = ' + var + ' = self.l' + str(m) + '(self.y' + str(m) + ')'
			else:
				cmd = 'self.yout = ' + var + ' = F.' + layer.activation + '(self.l' + str(m) + '(self.y' + str(m) + '))'
			exec(cmd)

		if torch.isnan(self.yout).any():
			print('\n nan was detected inside a network forward\n')
			import pdb; pdb.set_trace()

		return self.yout


def run_SGD(loss_function, model_parameters, trainLoader, device, 
				X_dataType=torch.FloatTensor, Y_dataType=torch.FloatTensor,
				model=None, lr=0.001, print_status=True, max_epoch=1000,
				on_new_epoch_call_back=None):

	optimizer = torch.optim.Adam(model_parameters, lr=lr)	
	scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau( optimizer, factor=0.5, min_lr=1e-10, patience=50, verbose=False)
	paramLen = len(signature(loss_function).parameters) # number of arguments

	if type(loss_function).__name__ == 'str':
		if loss_function == 'mse':
			loss_function = nn.MSELoss()
		elif loss_function == 'L1':
			loss_function = nn.L1Loss()


	for epoch in range(max_epoch):

		loss_list = []	
		for (i, data) in enumerate(trainLoader):
			[x, y, ind] = data

			x = Variable(x.type(X_dataType), requires_grad=False)
			y = Variable(y.type(Y_dataType), requires_grad=False)
			x= x.to(device, non_blocking=True )
			y= y.to(device, non_blocking=True )
			optimizer.zero_grad()
			
			if model is not None:
				ŷ = model(x)

				if paramLen == 4:
					loss = loss_function(x, y, ŷ, ind)
				elif paramLen == 3:
					loss = loss_function(x, y, ind)
				elif paramLen == 2:
					ŷ = torch.squeeze(ŷ)
					loss = loss_function(y, ŷ)
			else:
				try:
					loss = loss_function(x, y, ind)
				except:
					loss = loss_function(x, y)

			if torch.isnan(loss): import pdb; pdb.set_trace()

			loss.backward()
			optimizer.step()

			loss_list.append(loss.item())

		loss_avg = np.array(loss_list).mean()
		scheduler.step(loss_avg)
		if print_status:
			txt = '\tepoch: %d, Avg Loss: %.4f, Learning Rate: %.8f'%((epoch+1), loss_avg, scheduler._last_lr[0])
			write_to_current_line(txt)

		if on_new_epoch_call_back is not None:
			on_new_epoch_call_back(loss_avg, (epoch+1), scheduler._last_lr[0])

		if model is not None:
			if "on_new_epoch" in dir(model):
				early_exit = model.on_new_epoch(loss_avg, (epoch+1), scheduler._last_lr[0])
				if early_exit: break



class basicNetwork:
	def __init__(self, costFunction, X, 
						Y=None, networkStructure=[(3,'relu'),(3,'relu'),(3,'none')], 
						on_new_epoch_call_back = None, max_epoch=1000, 	X_dataType=torch.FloatTensor, 
						Y_dataType=torch.FloatTensor, learning_rate=0.001):
		'''
			possible activation functions: softmax, relu, tanh, sigmoid, none
		'''
		#	X should be in wuml format
		self.trainLoader = X.get_data_as('DataLoader')

		self.lr = learning_rate
		self.max_epoch = max_epoch
		self.X_dataType = X_dataType
		self.Y_dataType = Y_dataType
		self.costFunction = costFunction
		self.NetStructure = networkStructure
		self.on_new_epoch_call_back = on_new_epoch_call_back #set this as a callback at each function
		self.model = flexable_Model(X.shape[1], networkStructure)

		if torch.cuda.is_available(): 
			self.device = 'cuda'
			self.model.to(self.device)		# store the network weights in gpu or cpu device
		else: self.device = 'cpu'

		self.info()

	def info(self):
		print('Network Info:')
		print('\tLearning rate: %.3f'%self.lr)
		print('\tMax number of epochs: %d'%self.max_epoch)
		print('\tCost Function: %s'%str(self.costFunction))
		print('\tTrain Loop Callback: %s'%str(self.on_new_epoch_call_back))
		print('\tCuda Available: %r'%torch.cuda.is_available())
		print('\tNetwork Structure')
		for i in self.model.children():
			try:
				print('\t\t%s , %s'%(i,i.activation))
			except:
				print('\t\t%s '%(i))


	def __call__(self, data, output_type='Tensor'):
		if type(data).__name__ == 'ndarray': 
			x = torch.from_numpy(data)
			x = Variable(x.type(self.X_dataType), requires_grad=False)
			x= x.to(self.device, non_blocking=True )
		elif type(data).__name__ == 'Tensor': 
			x = Variable(x.type(self.X_dataType), requires_grad=False)
			x= x.to(self.device, non_blocking=True )
		elif type(data).__name__ == 'wData': 
			x = data.get_data_as('Tensor')
		else:
			raise

		yout = self.model(x)

		if output_type == 'ndarray':
			return yout.detach().cpu().numpy()

		return yout

	def train(self, print_status=True):
		param = self.model.parameters()
		[ℓ, TL, mE, Dev] = [self.costFunction, self.trainLoader, self.max_epoch, self.device]
		[Xtype, Ytype] = [self.X_dataType, self.Y_dataType]

		run_SGD(ℓ, param, TL, Dev, model=self.model, lr=self.lr, 
				max_epoch=mE, X_dataType=Xtype, Y_dataType=Ytype, 
				on_new_epoch_call_back = self.on_new_epoch_call_back)




