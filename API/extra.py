import os

file_path = "timepass.py"  # Change this to your actual file

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Keep only the first 2348 lines
    with open(file_path, "w") as file:
        file.writelines(lines[:2348])

    print(f"Deleted lines from 2349 onward in {file_path}")
else:
    print(f"Error: File '{file_path}' not found!")
