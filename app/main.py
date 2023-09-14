import os
import sys
from ai_analysis import analyze_directory
from file_handler import generate_txt

def main(directory, openai_key):
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory.")
    if not openai_key:
        raise ValueError("OpenAI key is not provided.")

    relevant_files = analyze_directory(directory, openai_key)
    generate_txt(relevant_files)

if __name__ == "__main__":
    directory = sys.argv[1]
    openai_key = sys.argv[2]
    main(directory, openai_key)