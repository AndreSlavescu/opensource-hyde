#!/bin/bash

# Define the environment name
ENV_NAME="opensource-hyde"

if ! command -v conda &> /dev/null
then
    echo "conda could not be found, please install it first."
    exit
fi

conda env create -f environment.yml -n $ENV_NAME

echo "Activating the environment: $ENV_NAME"
conda activate $ENV_NAME

echo "$ENV_NAME has been created and activated."
