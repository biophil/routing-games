# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 09:05:47 2016

@author: Philip
"""

import numpy as np
from linear import Network

t = Network(np.diag([1,2,3,4]),[1,2,3,4])
print(t.X)

XAXT = t.Y@t.A@t.Y.T # this is the matrix that tells us which direction z moves
# (if all b(i+1)-b(i)=1)