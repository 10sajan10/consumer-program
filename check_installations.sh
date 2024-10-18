#!/bin/bash

# Function to install Python
install_python() {
    echo "Installing Python..."
    sudo apt update
    sudo apt install -y python3 python3-pip
}

# Function to install AWS CLI
install_aws_cli() {
    echo "Installing AWS CLI..."
    sudo apt update
    sudo apt install -y awscli
}

# Check for Python installation
if command -v python3 &>/dev/null; then
    echo "Python is installed"
else
    echo "Python is not installed"
    install_python
fi

# Check for AWS CLI installation
if command -v aws &>/dev/null; then
    echo "AWS CLI is installed"
else
    echo "AWS CLI is not installed"
    install_aws_cli
fi
