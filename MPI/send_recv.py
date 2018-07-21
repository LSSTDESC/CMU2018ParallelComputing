#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    A = np.array([0, 1])
else:
    A = np.array([2, 3])

result = np.array(0)
buffer = np.array(0)

for i in range(2):
    result += A[i]

if rank == 0:
    comm.Recv(buffer, source=1)
    result += buffer
    print(result)

if rank == 1:
    comm.Send(result, dest=0)
