import os
import subprocess

# Set the directory where you want to download the file
download_dir = 'C:\Marek\Programming\Python\DataSentics\Downloads'

# Ensure the directory exists
os.makedirs(download_dir, exist_ok=True)

# Set the environment variable for Kaggle API key file location
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# Dataset information
dataset = 'arashnic/book-recommendation-dataset'
file_name = 'Ratings.csv'

# Construct the command to download the dataset
command = f'kaggle datasets download -d {dataset} -f {file_name} --path {download_dir} --unzip'

# Execute the command
subprocess.run(command, shell=True, check=True)

print(f'{file_name} has been downloaded to {download_dir}.')