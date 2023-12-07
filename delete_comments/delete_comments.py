import os

def remove_comments(input_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(input_file, "w", encoding="utf-8") as outfile:
        for line in lines:
            if not line.strip().startswith("#") or "TODO" in line:
                outfile.write(line)

def remove_comments_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".rpy"):
                input_file = os.path.join(root, filename)
                remove_comments(input_file)

directory_path = "."

remove_comments_from_directory(directory_path)
