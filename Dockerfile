FROM ubuntu
MAINTAINER EiffL

RUN apt-get update && \
    apt-get install -y autoconf automake gcc g++ make gfortran wget zlib1g-dev \
    python3-numpy python3-dev &&\
    apt-get clean all

# Make sure we are runnning python3
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN mkdir /build/

RUN cd /build && wget http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz \
  && tar xvzf mpich-3.2.tar.gz && cd /build/mpich-3.2 \
  && ./configure && make -j4 && make install && make clean && rm /build/mpich-3.2.tar.gz

RUN cd /build && wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.0.tar.gz \
  && tar xvzf mpi4py-3.0.0.tar.gz
RUN cd /build/mpi4py-3.0.0 && python3 setup.py build && python setup.py install && rm -rf /build/
RUN /sbin/ldconfig
