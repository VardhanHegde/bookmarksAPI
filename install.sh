#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python-is-python3 -y

sudo apt install python3-pip -y

sudo apt install virtualenv -y

virtualenv --python=python3.12 env 
source env/bin/activate

pip install -r requirements.txt 

flask run
