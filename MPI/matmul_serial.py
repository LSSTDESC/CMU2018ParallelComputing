#!/usr/bin/env python
import numpy as np
import h5py
import time

# Open the data file
with h5py.File('data.hdf', 'r') as f:
    A = f['A'][:]
    B = f['B'][:]

t0 = time.time()  # start time
C = np.dot(A,B)
t1 = time.time() # end time
print("Numpy matrix multiplication took: %f ms"%((t1-t0)*1000))
