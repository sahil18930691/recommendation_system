#!/bin/bash
pip install -r requirements.txt

if [ $? -eq 0 ]
then
    uvicorn main:app --reload &
else
    echo "Failed to install dependencies"
fi
