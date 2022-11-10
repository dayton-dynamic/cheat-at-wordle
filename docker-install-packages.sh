#!/bin/bash
# Modified from example at https://pythonspeed.com/articles/system-packages-docker/
# The goal of this script is to cleanly
# 1) Grab security updates pertinant to the Docker image from within which this script is called
# 2) Install cURL, a needed dependency
# 3) Clean the package cache (etc)
# in such a way that Docker caching is preserved and unneeded files are never present in any layer of the image

# Bash "strict mode", to help catch problems and bugs in the shell script. Every bash script you write should include this. See
set -euo pipefail

# Tell apt-get we're never going to be able to give manual feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get -y -qq -o=Dpkg::Use-Pty=0 update

# Install security updates:
apt-get -y -q -o=Dpkg::Use-Pty=0 upgrade

# Install cURL (needed for Poetry install)
apt-get -y -qq install --no-install-recommends -o=Dpkg::Use-Pty=0 curl

# Install American English dict
apt-get -y -qq install --no-install-recommends -o=Dpkg::Use-Pty=0 wamerican

# Delete cached files we don't need anymore (note that if you're
# using official Docker images for Debian or Ubuntu, this happens
# automatically, you don't need to do it yourself):
apt-get clean
# Delete index files we don't need anymore:
rm -rf /var/lib/apt/lists/*
