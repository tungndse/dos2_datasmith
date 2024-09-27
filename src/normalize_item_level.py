import os
import threading

# Create a lock for thread-safe file writing
file_lock = threading.Lock()

def update_act_part(file_path):
    """Update 'Act part' in the file if it's greater than 5."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if 'data "Act part"' in line:
            # Extract the current Act part value
            part_value = int(line.split('"')[3])
            line = f'data "Act part" "1"\n'

        updated_lines.append(line)

    # Write changes back to the file
    with file_lock:
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)

def process_files_in_folder(folder_path):
    """Process both armor.txt and weapon.txt in the folder."""
    target_files = ['armor.txt', 'weapon.txt']
    threads = []

    for file_name in target_files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            thread = threading.Thread(target=update_act_part, args=(file_path,))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Processing complete for folder: {folder_path}")

# Example usage
folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUniques_173e1939-2e97-1467-c7db-02a7b33aa786\Public\BonusUniques_173e1939-2e97-1467-c7db-02a7b33aa786\Stats\Generated\Data'
process_files_in_folder(folder_path)
