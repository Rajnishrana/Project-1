import os
import re

class DataPreprocessor:
    def __init__(self, raw_data_path, processed_data_path):
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path

    def load_raw_dialogs(self):
        lines_file = os.path.join(self.raw_data_path, "movie_lines.txt")
        convs_file = os.path.join(self.raw_data_path, "movie_conversations.txt")

        id2line = {}
        with open(lines_file, 'r', encoding='iso-8859-1') as f:
            for line in f:
                parts = line.strip().split(" +++$+++ ")
                if len(parts) == 5:
                    id2line[parts[0]] = parts[4]

        pairs = []
        with open(convs_file, 'r', encoding='iso-8859-1') as f:
            for line in f:
                parts = line.strip().split(" +++$+++ ")
                if len(parts) == 4:
                    line_ids = eval(parts[3])
                    for i in range(len(line_ids) - 1):
                        input_line = id2line.get(line_ids[i], "")
                        response_line = id2line.get(line_ids[i+1], "")
                        if input_line and response_line:
                            pairs.append((input_line, response_line))
        return pairs

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9?.!,']+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def preprocess_and_save(self):
        print("Loading raw dialogs...")
        pairs = self.load_raw_dialogs()
        print(f"Loaded {len(pairs)} pairs")

        cleaned_pairs = []
        for input_line, response_line in pairs:
            input_line = self.clean_text(input_line)
            response_line = self.clean_text(response_line)
            if input_line and response_line:
                cleaned_pairs.append(f"{input_line}\t{response_line}")

        os.makedirs(os.path.dirname(self.processed_data_path), exist_ok=True)

        print(f"Saving {len(cleaned_pairs)} cleaned pairs to {self.processed_data_path}")
        with open(self.processed_data_path, 'w', encoding='utf-8') as f:
            for line in cleaned_pairs:
                f.write(line + "\n")
        print("Preprocessing completed.")

if __name__ == "__main__":
    raw_path = "data/raw/archive(3)"
    processed_path = "data/processed/cleaned_dialogs.txt"

    preprocessor = DataPreprocessor(raw_path, processed_path)
    preprocessor.preprocess_and_save()
