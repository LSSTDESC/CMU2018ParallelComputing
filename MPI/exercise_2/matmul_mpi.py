from mpi4py import MPI
import numpy as np
import h5py
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Open the data file
with h5py.File('data.hdf', 'r', driver='mpio', comm=MPI.COMM_WORLD) as f:
    A_dset = f['A']
    B_dset = f['B']

    A = np.empty(A_dset.shape, A_dset.dtype)
    with A_dset.collective:
       A[:] = A_dset[:]

    nx, ny = B_dset.shape
    block_size = ny // size
    start = rank * block_size
    end = (rank + 1) * block_size
    B = np.empty((nx, block_size), B_dset.dtype)
    with B_dset.collective:
       B[:] = B_dset[:, start:end]

C = np.empty((A.shape[0], ny), dtype=np.float32)
buffer = np.empty((A.shape[0], B.shape[1]), dtype=np.float32)

# Waiting for all processes to be ready
comm.Barrier()
t0 = time.time()  # start time

#Compute the local dot product
C[:, start:end] = np.dot(A, B)

buffer[:] = C[:, rank * block_size:(rank + 1) * block_size]

source_rank = (rank + 1) % size
dest_rank = (rank - 1) % size

for i in range(size - 1):
    comm.Sendrecv_replace(buffer, dest=dest_rank, source=source_rank)
    C[:, ((source_rank + i) % size) * block_size:(((source_rank + i) % size) + 1) * block_size] = buffer

t1 = time.time() # end time

print("MPI matrix multiplication took %f ms" %((t1-t0)*1000.))
