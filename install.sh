#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export FLASK_APP=bikeservice
flask init-db
