# -*- coding: utf-8 -*-
"""iris dataset in logistic regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DebBMxXQsqfr9fSqAzhWyrkd0pO5dpqy
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# %matplotlib inline

iris = load_iris()

print(iris.DESCR)

features = pd.DataFrame(iris.data, columns = iris.feature_names)
target = pd.DataFrame(iris.target, columns = ['Target'])
data = pd.concat([features, target],axis = 1)

a=data.corr('pearson')
abs(a.loc['Target']).sort_values(ascending = False)

x = np.array(data['petal width (cm)'])
y = np.array(data['Target'])

x = x/x.mean()

plt.plot(x,y,'r.')

n = int(0.8* len(x))
x_train = x[:n]
y_train = y[:n]

x_test = x[n:]
y_test = y[n:]

def sigmoid(x):
  return 1/(1+np.exp(-x))

def error(a,b,x,y):
  error = 0
  m = len(x)
  for i in range(m):
    z = a*x[i] + b
    error += y[i] * np.log(sigmoid(z)) + (1-y[i])*np.log(1-sigmoid(z))
  return (-1/m) *error

def step_gradient(a,b,x,y,learning_rate):
  grad_a = 0
  grad_b = 0
  m = len(x)
  for i in range(m):
    z = a*x[i] + b
    grad_a += 1/m * (sigmoid(z)-y[i])*x[i]
    grad_b += 1/m * (sigmoid(z)-y[i])
  a = a - (grad_a * learning_rate)
  b = b - (grad_b * learning_rate)

  return a,b

def descend(initial_a,initial_b,x,y,learning_rate,iterations):
  a=initial_a
  b=initial_b
  for i in range(iterations):
    e=error(a,b,x,y)
    if i%1000 ==0:
      print(f'Error: {e}')
    a,b=step_gradient(a,b,x,y,learning_rate)
  return a,b

def accuracy(theta,a,b,x,y):
  count=0
  for j in range(len(x)):
    test = sigmoid(theta)

    if test[j]>0.9:
      z=1
    else:
      z=0
    if y[j]==z:
      count += 1
  acc = count/len(y)
  print(f"Error is {100-(acc*100)}")

a = 1
b = 1
learning_rate = 0.01
iterations = 10000
final_a,final_b = descend(a,b,x_train,y_train,learning_rate,iterations)

f = final_a*x_train+final_b
plt.plot(x_train,y_train,'r.',x_train,sigmoid(f),'b.')

g=final_a*x_test+final_b
plt.plot(x_test,y_test,'g.',x_test,sigmoid(g),'co')

accuracy(f, final_a, final_b, x_train, y_train)
accuracy(g, final_a, final_b, x_test, y_test)
