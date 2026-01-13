#!/bin/bash
#Generate keys to make master access other nodes via ssh

# exits on errors
set -e

echo "Container starting with hostname: $HOSTNAME"

mkdir -p /shared/home /shared/data

mkdir -p /root/.ssh

MASTER_PUB="/shared/master.pub"


if [ "$HOSTNAME" = "master" ]; then

    if [ ! -f /root/.ssh/id_rsa ]; then
        echo "Generating SSH key pair..."
        ssh-keygen -t rsa -q -N "" -f /root/.ssh/id_rsa
    fi

    # Copy public key to shared volume
    cp /root/.ssh/id_rsa.pub "$MASTER_PUB"
    echo "Master public key written to $MASTER_PUB"

else
    echo "Waiting for master public key..."
    while [ ! -f "$MASTER_PUB" ]; do
        sleep 1
    done

    cat "$MASTER_PUB" >> /root/.ssh/authorized_keys
    echo "Master public key added to /root/.ssh/authorized_keys"
fi

# Set secure permissions for the key files
chmod 700 /root/.ssh
chmod 600 /root/.ssh/*


echo "Container setup complete. Starting SSH Daemon..."
# Start SSHD and keep container running
exec /usr/sbin/sshd -D

