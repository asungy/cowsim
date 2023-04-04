FROM ubuntu:22.04

# Install apt packages.
RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-pip \
        python3.10-venv \
    && apt-get clean

# Install pip packages.
RUN pip install --upgrade \
        build \
        setuptools \
    && :

# Default command
CMD /bin/bash
