#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    A = np.array([0, 1, 2, 3, 4], dtype=np.int32)
else:
    A = np.zeros(5, dtype=np.int32)

if rank == 0:
    comm.Bcast(A, root=0)
print("I am process %d:" % rank, A)
