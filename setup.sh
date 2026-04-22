#!/bin/bash

#system dependencies
brew install python@3.11
brew install glui
brew install cddlib

#create virtual environment and activate
python3.11 -venv venv
source venv/bin/activate

#Python dependencies
pip install -r requirements.txt