# Use the official Ubuntu base image
FROM python

RUN apt-get update && apt-get install -y \
    libvirt-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install packages
RUN pip install pymongo requests libvirt-python

# Create the file directory
RUN mkdir /opt/vmazing
RUN mkdir /var/run/

# Set the default command to keep the container running
CMD ["bash", "-c", "while true; do sleep 30; done;"]