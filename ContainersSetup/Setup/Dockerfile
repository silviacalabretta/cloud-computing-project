FROM ubuntu:22.04

# Set non-interactive mode for automated installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        openssh-server \
        sudo \
        stress-ng \
        sysbench \
        iozone3 \
        iperf3 \
        netcat \
        openmpi-bin \
        libopenmpi-dev \
        hpcc \
        git \
        build-essential \
        python3 \
        libtool \
        pkg-config \
        automake \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- SSH Setup ---
RUN mkdir /var/run/sshd
# Generate necessary SSH host keys at build time
RUN ssh-keygen -A
# NO: Allow root login (required for simple testing environment)
# RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
# MAYBE: Do not use PAM, which can cause issues in minimal container environments
# RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

# RUN mkdir -p /root/.ssh
# RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -N ""
# RUN cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys
# RUN chmod 600 /root/.ssh/authorized_keys

# Configure the root user's SSH to trust all hosts (useful for testing)
RUN echo "Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile /dev/null" > /root/.ssh/config
RUN chmod 600 /root/.ssh/config

# Copy all the testing files
# COPY Performance_Testing/ ./Performance_Testing/

# Copy benchmark scripts into the image
COPY benchmarks/ /root/benchmarks/

# Make them executable
RUN chmod +x /root/benchmarks/*.sh

# Copy the runtime startup script and make it executable
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Expose the default SSH port (internal to the network)
EXPOSE 22

# Set the entrypoint to the startup script which generates user keys and starts sshd
ENTRYPOINT ["/usr/local/bin/start.sh"]


