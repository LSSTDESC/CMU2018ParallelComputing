#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    A = [0, 1]

if rank == 1:
    A = [2, 3]

result = 0
for i in range(2):
    result += A[i]

if rank == 0:
    res = comm.recv(source=1)
    result = res + result
    print(result)

if rank == 1:
    comm.send(result, dest=0)
