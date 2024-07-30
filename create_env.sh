#!/bin/bash

ENV_NAME="opensource-hyde"

if ! command -v conda &> /dev/null; then
    echo "conda could not be found, please install it first."
    exit 1
fi

if ! command -v javac &> /dev/null; then
    echo "JDK could not be found, please install it first."
    exit 1
fi

export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
echo "JAVA_HOME set to $JAVA_HOME"
export PATH=$PATH:$JAVA_HOME/bin
echo "PATH updated to include $JAVA_HOME/bin"

if conda env list | grep -q "^$ENV_NAME\s"; then
    echo "Environment $ENV_NAME already exists. Skipping creation."
else
    conda env create -f environment.yml -n $ENV_NAME
    if [ $? -eq 0 ]; then
        echo "Environment $ENV_NAME created successfully."
    else
        echo "Failed to create environment $ENV_NAME."
        exit 1
    fi
fi

eval "$(conda shell.bash hook)"

echo "Activating the environment: $ENV_NAME"
conda activate $ENV_NAME

if [ $? -eq 0 ]; then
    echo "$ENV_NAME has been activated."
else
    echo "Failed to activate environment $ENV_NAME."
    exit 1
fi

echo "Java version: $(java -version)"
echo "javac version: $(javac -version)"
