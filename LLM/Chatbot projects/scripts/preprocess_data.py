import sys
import os

# Add root project path to sys.path so imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.prepare_data import DataPreprocessor

def run_preprocessing():
    raw_path = "data/raw/archive(3)"  # Path where raw data is stored
    processed_path = "data/processed.txt"  # Output file path

    print("Starting preprocessing...")
    preprocessor = DataPreprocessor(raw_path, processed_path)
    preprocessor.preprocess_and_save()
    print("Preprocessing finished.")

if __name__ == "__main__":
    run_preprocessing()
