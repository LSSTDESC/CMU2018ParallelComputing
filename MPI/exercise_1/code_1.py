#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

A = np.array([2 * rank, 2 * rank + 1])

result = 0
for i in range(size):

    source_rank = (rank + 1) % size
    dest_rank = (rank - 1) % size

    comm.Recv(A, source_rank)

    result += np.sum(A)

    comm.Send(A, dest_rank)

print("Process %d, computed: %d" % (rank, result))
