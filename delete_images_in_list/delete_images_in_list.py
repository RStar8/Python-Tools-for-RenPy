import os

def delete_files_in_directory(directory, file_names_to_delete):
    deleted_count = 0
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_name_without_path = os.path.basename(file_name)
            file_name_without_extension = os.path.splitext(file_name_without_path)[0]

            if file_name_without_extension in file_names_to_delete:
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1

    return deleted_count

folder_to_search = "images"
list_file_path = "unused_images.txt"

try:
    with open(list_file_path, "r") as file:
        first_line = file.readline()
        print("First line:", first_line)
        image_file_names_to_delete = file.read().splitlines()

    deleted_count = delete_files_in_directory(folder_to_search, image_file_names_to_delete)
    print(f"Deletion complete. {deleted_count} files deleted.")
except FileNotFoundError:
    print(f"File not found: {list_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")