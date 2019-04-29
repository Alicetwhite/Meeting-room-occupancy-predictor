#This script draws different activation function graphs

import math

def sigmoid(x):
    y= []
    for item in x:
        y.append(1/(1+math.exp(-item)))
    return y

def tanh(x):
    y= []
    for item in x:
        y.append( 2/(1+math.exp(-2*item)) -1 )
    return y

def relu(x):
    y= []

    for item in x:
        y.append(max(0,item))

    return y

def linear(x):
    y = []

    for item in x:
        y.append(item)
    return y

import matplotlib.pyplot as plt
import numpy as np


x = np.arange(-10., 10., 0.2)
sig = sigmoid(x)
tanh = tanh(x)
relu = relu(x)
linear = linear(x)
plt.plot(x,linear)
plt.show()
