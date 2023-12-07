import os
import re

def extract_image_names(line):
    image_names = []

    match = re.search(r'^\s*(?:scene|show)\s*([^:\n]*?(?=\s+(?:with |at )\b|:|$))', line)
    if match:
        image_name = match.group(1)
        image_names.append(image_name.strip('"\''))

    matches = re.findall(r'"([^"]+\.(?:png|webp|jpg))"', line)
    for match in matches:
        name = match.strip().split('/')[-1]
        name = name.split('.')[0]
        image_names.append(name)

    matches = re.findall(r'"([^"]+?)"', line)
    for match in matches:
        if '.' not in match:
            image_names.append(match)

    return image_names

def is_commented(line):
    return line.strip().startswith('#')

def normalize_path(path):
    return os.path.normpath(path)

def find_unused_images(code_directory, image_directory):
    unused_images = {}
    code_images = {}

    for root, dirs, files in os.walk(code_directory):
        for file in files:
            if file.endswith('.rpy'):
                code_file_path = os.path.join(root, file)
                with open(code_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not is_commented(line):
                            code_image_names = extract_image_names(line)
                            if code_file_path not in code_images:
                                code_images[code_file_path] = set()
                            code_images[code_file_path].update(
                                code_image_names)

    for root, dirs, files in os.walk(image_directory):
        for file in files:
            if file.endswith(('.png', '.webp', '.jpg')):
                image_file_path = os.path.join(root, file)
                image_file_relpath = os.path.relpath(
                    image_file_path, image_directory)
                image_file_relpath_normalized = normalize_path(
                    image_file_relpath)

                image_name = os.path.splitext(
                    os.path.basename(image_file_relpath_normalized))[0]

                found_in_code = False
                for code_file_path, code_image_names in code_images.items():
                    if image_name in code_image_names:
                        found_in_code = True
                        break

                if not found_in_code:
                    folder_name = os.path.dirname(image_file_relpath)
                    if folder_name not in unused_images:
                        unused_images[folder_name] = []
                    unused_images[folder_name].append(image_name)

    return unused_images, code_images

unused_images, code_images = find_unused_images('code', 'images')

with open('unused_images.txt', 'w', encoding='utf-8') as f:
    f.write('List of Unused Images:\n')
    for folder_name, image_names in sorted(unused_images.items()):
        f.write('-' * 40)
        f.write(f'\nFolder: {folder_name}\n')
        f.write('-' * 40 + '\n')
        for image in sorted(image_names):
            f.write(image + '\n')

# with open('code_images.txt', 'w', encoding='utf-8') as f:
#     f.write('List of Images Found in Code:\n')
#     for code_file_path, code_image_names in sorted(code_images.items()):
#         f.write('-' * 40)
#         f.write(f'\nCode File: {code_file_path}\n')
#         f.write('-' * 40 + '\n')
#         for image in sorted(code_image_names):
#             f.write(image + '\n')
