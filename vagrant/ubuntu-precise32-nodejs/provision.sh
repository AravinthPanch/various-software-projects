#!/bin/bash

# Author: Aravinth Panchadcharam
# Email: me@aravinth.info
# Date: 26/03/14.
# Description: Provision NodeJS for Vagrant Box ubuntu-precise32


# Core Packages
apt-get update
apt-get install -y make g++ git curl vim

# NodeJS
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs

