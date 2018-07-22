#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    A = np.arange(4 * size, dtype=np.int32)
else:
    A = None

# Allocate arrays for communication
a = np.empty((4,), dtype=np.int32)
result = np.array(0, dtype=np.int32)

# Distributes chunks of size 4 accross all the processes
comm.Scatter(A, a, root=0)

# Perform local sum over chunk of array A
buff = np.array(np.sum(a**2), dtype=np.int32)

# Sums values and shares result with all processes
comm.Allreduce(buff, result, op=MPI.SUM)

if rank == 0:
    print("Norm of input array %f " % np.sqrt(np.sum(A**2)))
if rank == 1:
    print("Norm computed with MPI %f" % np.sqrt(result))
