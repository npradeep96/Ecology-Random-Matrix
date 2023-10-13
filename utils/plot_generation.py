"""
Module that contains functions to plot and analyze community matrices associated with different ecosystems
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator

# Set my favorite settings for plots
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
plt.rcParams['xtick.labelsize']=20
plt.rcParams['ytick.labelsize']=20
plt.rcParams['font.size']=20
plt.rcParams["text.usetex"]=True

### Function to plot adjacency matrix

def plot_adjacency_matrix(A, axes):
	""" Function that plots the adjacency matrix of an array containing either 
	(a) 0's and 1's or
	(b) 0's, 1's and -1's
	
	:param A: adjacency matrix
	:param axes: matplotlib axes object
	:type A: boolean or int numpy 2darray
	:type axes: axes object
	
	:return plot_obj: handle to the plotted object

	"""
	
	if np.min(A) == 0.0:
		# matrix of 0's and 1's
		plot_obj = axes.imshow(A)
		plot_obj.set_cmap("Reds")
		divider = make_axes_locatable(axes)
		colorbar_axes = divider.append_axes("right", size="10%", pad=0.1)
		plt.colorbar(plot_obj, ticks=range(2), label='Connection', cax=colorbar_axes)
		axes.xaxis.set_major_locator(MaxNLocator(3))
		axes.yaxis.set_major_locator(MaxNLocator(3))
		return plot_obj
	elif np.min(A) == -1.0:
		# matrix of 0's and 1's and -1's
		plot_obj = axes.imshow(A)
		plot_obj.set_cmap("RdBu_r")
		divider = make_axes_locatable(axes)
		colorbar_axes = divider.append_axes("right", size="10%", pad=0.1)
		plt.colorbar(plot_obj, ticks=np.arange(3)-1, label='Connection', cax=colorbar_axes)
		axes.xaxis.set_major_locator(MaxNLocator(3))
		axes.yaxis.set_major_locator(MaxNLocator(3))
		return plot_obj

### Function to plot community matrix

def plot_community_matrix(W, axes):
	"""Function that plots the community matrix of an array containing either 
	
	(a) all positive elements
	
	(b) a mixture of positive and negative elements
	
	:param W: community matrix
	:param axes: matplotlib axes object
	:type W: float numpy 2darray
	:type axes: axes object
	
	:return plot_obj: handle to the plotted object
	"""
	if np.min(W) == 0.0:
		# matrix of positive numbers
		plot_obj = axes.imshow(W-np.diag(np.diag(W)))
		plot_obj.set_cmap("Reds")
		divider = make_axes_locatable(axes)
		colorbar_axes = divider.append_axes("right", size="10%", pad=0.1)
		plt.colorbar(plot_obj, label='Interaction strength', cax=colorbar_axes)
		axes.xaxis.set_major_locator(MaxNLocator(3))
		axes.yaxis.set_major_locator(MaxNLocator(3))
		return plot_obj
	else:
		# matrix that includes negative entries
		range_min = np.mean(W) - np.std(W)
		range_max = np.mean(W) + np.std(W)
		plot_obj = axes.imshow(W-np.diag(np.diag(W)), vmin=range_min,vmax=range_max)
		plot_obj.set_cmap("RdBu_r")
		divider = make_axes_locatable(axes)
		colorbar_axes = divider.append_axes("right", size="10%", pad=0.1)
		plt.colorbar(plot_obj, label='Interaction strength', cax=colorbar_axes)
		axes.xaxis.set_major_locator(MaxNLocator(3))
		axes.yaxis.set_major_locator(MaxNLocator(3))
		return plot_obj

## Function to plot eigenvalue scatter plot

def scatter_plot_eigenvalues(eigenvals, axes, xrange=None, yrange=None):
	"""Function that plots a scatter plot of eigenvalues in the real and imaginary space
	
	:param eigenvals: array of complex valued eigenvalues
	:param xrange: a 2x1 containing [xmin, xmax]
	:param yrange: a 2x1 containing [ymin, ymax]
	:param axes: matplotlib axes object
	:type eigenvals: float numpy 1darray
	:type xrange: 2x1 list
	:type yrange: 2x1 list
	:type axes: axes object
	
	:return plot_obj: handle to the plotted object
	"""
	N = np.size(eigenvals)
	real_part = np.real(eigenvals)
	imaginary_part = np.imag(eigenvals)
	plot_obj = axes.scatter(x=real_part, y=imaginary_part, c=np.random.rand(N))
	min_val = np.min([real_part, imaginary_part])
	max_val = np.max([real_part, imaginary_part])
	if xrange == None:
		axes.set_xlim([min_val, max_val])
	else:
		axes.set_xlim(xrange)
	if yrange == None:
		axes.set_ylim([min_val, max_val])
	else:
		axes.set_ylim(yrange)
	axes.set_xlabel(r'Re($\lambda$)')
	axes.set_ylabel(r'Im($\lambda$)')
	axes.xaxis.set_major_locator(MaxNLocator(3))
	axes.yaxis.set_major_locator(MaxNLocator(3))
	axes.set_aspect('equal', adjustable='box')
	return plot_obj    
