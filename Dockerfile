FROM ubuntu
MAINTAINER EiffL

RUN apt-get update && \
    apt-get install -y dpkg-dev autoconf automake gcc g++ make gfortran wget zlib1g-dev \
    python3-numpy python3-dev git cython3 &&\
    apt-get clean all

# Make sure we are runnning python3
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN mkdir /build/

RUN cd /build && wget http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz \
  && tar xvzf mpich-3.2.tar.gz && cd /build/mpich-3.2 \
  && ./configure && make -j4 && make install && make clean && rm /build/mpich-3.2.tar.gz

RUN cd /build && wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.0.tar.gz \
  && tar xvzf mpi4py-3.0.0.tar.gz
RUN cd /build/mpi4py-3.0.0 && python3 setup.py build && python setup.py install

ENV HDF5_MINOR_REL       hdf5-1.10.1
ENV HDF5_SRC_URL         http://www.hdfgroup.org/ftp/HDF5/releases

RUN cd /build/ && \
    wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.1/src/hdf5-1.10.1.tar.gz ; \
    tar -xvzf hdf5-1.10.1.tar.gz  --directory /usr/local/src                      ; \
    cd /usr/local/src/hdf5-1.10.1                                                  ; \
    ./configure --prefix=/usr/local/hdf5 --enable-parallel --enable-shared         ; \
    make                                                                           ; \
    make install                                                                   ; \
    for f in /usr/local/hdf5/bin/* ; do ln -s $f /usr/local/bin ; done

RUN cd /build/ && \
    git clone https://github.com/h5py/h5py.git                                     ; \
    cd h5py                                                                        ; \
    export CC=mpicc                                                                ; \
    export HDF5_DIR=/usr/local/hdf5                                                ; \
    python setup.py configure --mpi                                                ; \
    python setup.py build                                                          ; \
    python setup.py install && rm -rf /build/

RUN /sbin/ldconfig

ADD . /deschool
