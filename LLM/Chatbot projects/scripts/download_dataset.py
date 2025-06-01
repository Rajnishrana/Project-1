import os
import subprocess

def download_kaggle_dataset(dataset_name, output_dir):
    """
    Downloads a dataset from Kaggle using the Kaggle CLI.
    
    Args:
        dataset_name (str): Kaggle dataset identifier, e.g., "cornell/movie-dialogs-corpus"
        output_dir (str): Directory where the dataset will be downloaded and extracted
    """
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_json_path):
        raise FileNotFoundError(f"Missing kaggle.json at {kaggle_json_path}. Place your credentials there.")

    os.makedirs(output_dir, exist_ok=True)
    command = [
        "kaggle", "datasets", "download", "-d", dataset_name,
        "-p", output_dir, "--unzip"
    ]
    subprocess.run(command, check=True)
    print(f"Downloaded and extracted dataset to {output_dir}")

if __name__ == "__main__":
    dataset = "cornell/movie-dialogs-corpus"
    output_directory = "data/raw/archive(3)"

    download_kaggle_dataset(dataset, output_directory)
