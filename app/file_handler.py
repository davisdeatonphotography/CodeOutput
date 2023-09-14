def generate_txt(relevant_files):
    with open('output.txt', 'w') as f:
        for file_path, content in relevant_files:
            f.write(f"File: {file_path}\nContent:\n{content}\n\n")
