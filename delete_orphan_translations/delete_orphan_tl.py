import os
import re

def delete_orphan_translations(lint_report_file, base_directory):
    with open(lint_report_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    deletion_ranges = []
    updated_lines = []
    for line in lines:
        line = line.strip()
        match = re.search(r'([^:]+) : this file contains orphan translations at lines?\s(\d+)', line)

        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))
            full_path = os.path.join(base_directory, file_path)

            start_line = max(1, line_number - 2)
            end_line = min(line_number + 3, get_file_length(full_path) + 1)
            deletion_ranges.append((full_path, start_line, end_line))

        else:
            updated_lines.append(line)

    for deletion_range in deletion_ranges:
        file_path, start_line, end_line = deletion_range

        with open(file_path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()

        del file_lines[start_line - 1:end_line]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(file_lines)

        print(f"Deleted lines {start_line}-{end_line} in file: {file_path}")

    with open(lint_report_file, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

def get_file_length(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return len(lines)

lint_report_file = 'C:/Users/debtr/Downloads/lint.txt'
base_directory = 'D:/Workspace/ViNovella/FLW2/'
delete_orphan_translations(lint_report_file, base_directory)
