import os
import subprocess
import kaggle


def download_kaggle():
    try:
        download_dir = r"C:\Marek\Programming\Python\DataSentics\Kaggle downloads"

        # Ensure the directory exists
        os.makedirs(download_dir, exist_ok=True)

        # Set the environment variable for Kaggle API key file location
        kaggle_config_dir = os.path.expanduser('~/.kaggle')
        if not os.path.exists(kaggle_config_dir):
            raise FileNotFoundError(f"Kaggle configuration directory '{kaggle_config_dir}' does not exist.")

        os.environ['KAGGLE_CONFIG_DIR'] = kaggle_config_dir

        # Authenticate using the API token
        kaggle.api.authenticate()

        # Dataset information
        dataset = 'arashnic/book-recommendation-dataset'
        file_name = 'Ratings.csv'

        # Download the dataset
        kaggle.api.dataset_download_files(dataset, path=download_dir, unzip=True)
        print(f'{file_name} has been downloaded to {download_dir}.')

    except FileNotFoundError as fnfe:
        print(f"FileNotFoundError: {fnfe}")
    except Exception as e:
        print(f"An error occurred: {e}")
