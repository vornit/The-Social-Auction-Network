#!/bin/sh

# This file is ran after devcontainer is created.

# Copy kube config to the container
echo "source $PWD/.devcontainer/copy-kube-config.sh" | tee -a $HOME/.bashrc $HOME/.zshrc >> /dev/null
