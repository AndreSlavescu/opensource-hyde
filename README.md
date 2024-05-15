# HyDE on Open Source Models

## Building Environment

Below are the steps to build project environment:

1. Ensure you have `conda`. If not installed, you may install it from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

2. Make `create_env.sh` executable:
   ```bash
   chmod +x create_env.sh
   ```

3. Run the script to create and activate the environment:
   ```bash
   ./create_env.sh
   ```

4. Make sure to export your huggingface_token:
   ```bash
   export HUGGINGFACE_TOKEN="your token"
   ```

A new conda environment named `opensource-hyde` will be automatically created for you with all required dependencies listed in `environment.yml`, and activated accordingly.
