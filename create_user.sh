#!/bin/bash

# Check if script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root!" >&2
    exit 1
fi

# Get user input
read -p "Enter username: " username
read -p "Enter full name: " fullname
read -s -p "Enter initial password: " password
echo

# Create the user
useradd -m -c "$fullname" -s /bin/bash "$username"

# Set the initial password
echo "$username:$password" | chpasswd

passwd --expire "$username"

if [[ $? -ne 0 ]]; then
    echo "Error: User creation failed!" >&2
    exit 1
fi


echo "User account successfully created!"
echo "----------------------------------"
echo "Username: $username"
echo "Full Name: $fullname"
echo "Hostname: $(hostname)"
