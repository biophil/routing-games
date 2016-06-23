# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 09:05:47 2016

@author: Philip
"""

from numpy import array, diag
from linear import Network

t = Network(diag([1,2,3,4]),[1,2,3,4])
print(t.X)