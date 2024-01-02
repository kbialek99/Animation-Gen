import os

def sort_and_rename(folder_path):
    files = [file for file in os.listdir(folder_path) if file.lower().endswith('.png')]
    sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True)

    for index, file in enumerate(sorted_files, start=1):
        original_path = os.path.join(folder_path, file)
        new_name = f"{index:03d}_{file}"  # Using three digits for the index, e.g., 001_filename.png
        new_path = os.path.join(folder_path, new_name)

        os.rename(original_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

if __name__ == "__main__":
    folder_path = os.getcwd()  # Get the current working directory
    sort_and_rename(folder_path)