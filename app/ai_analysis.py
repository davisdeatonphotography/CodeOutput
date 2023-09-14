import os
import openai
from datetime import datetime
from radon.complexity import cc_visit
from radon.metrics import h_visit

def analyze_directory(directory, openai_key):
    openai.api_key = openai_key
    relevant_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Skip files that cannot be decoded with utf-8 encoding
                continue

            size = os.path.getsize(file_path)
            last_modified = os.path.getmtime(file_path)
            last_modified_date = datetime.fromtimestamp(last_modified)

            # Criteria for relevancy
            is_relevant = (
                is_relevant_size(size) and
                is_relevant_content(content, openai_key) and
                is_recently_modified(last_modified_date) and
                is_relevant_location(root)
            )

            if is_relevant:
                relevant_files.append((file_path, content))

    return relevant_files

def is_relevant_size(size):
    return size > 1000 and size < 1000000

def is_relevant_content(content, openai_key):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"How relevant is this content on a scale of 1-10?\n\n{content}"}
            ]
        )
        score = int(response['choices'][0]['message']['content'].strip())
        return score >= 5
    except Exception as e:
        print(f"Error in API call: {e}")
        return False

def is_recently_modified(last_modified_date):
    return (datetime.now() - last_modified_date).days < 180

def is_relevant_location(root):
    return 'src' in root

def has_frequent_changes(file_path, repo):
    commits = list(repo.iter_commits(paths=file_path))
    return len(commits) > 10
