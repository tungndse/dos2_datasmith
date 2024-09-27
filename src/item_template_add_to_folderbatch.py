import os


def process_files_in_folder(folder_path, quantity):
    # Dictionary to store commands grouped by school
    school_commands = {}
    ungrouped_commands = []

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            file_school_commands, file_ungrouped_commands = process_skillbooks(file_path, quantity)  # Process each file

            # Update the main dictionary with file data
            for school, commands in file_school_commands.items():
                if school not in school_commands:
                    school_commands[school] = []
                school_commands[school].extend(commands)

            ungrouped_commands.extend(file_ungrouped_commands)

    # Output results
    output_file = os.path.join(folder_path, 'processed_commands.txt')
    with open(output_file, 'w') as file:
        for school, commands in school_commands.items():
            file.write(f'// {school.upper()}\n')
            for command in commands:
                file.write(f'{command}\n')
            file.write('\n')

        if ungrouped_commands:
            file.write('// UNGROUPED\n')
            for command in ungrouped_commands:
                file.write(f'{command}\n')

    print(f"Commands processed and saved to {output_file}")


def process_skillbooks(file_path, quantity):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Dictionary to store commands grouped by school
    school_commands = {}
    ungrouped_commands = []

    # Process each line in the file
    entry_data = {}
    entry_name = None
    entry_type = None

    for line in lines:
        line = line.strip()
        if line.startswith('new entry'):
            entry_name = line.split('"')[1]
            entry_data = {}
        elif line.startswith('type'):
            entry_type = line.split('"')[1]
        elif line.startswith('using'):
            entry_using = line.split('"')[1]
        elif line.startswith('data'):
            key, value = line.split('"')[1::2]
            entry_data[key] = value
        elif line == '':
            if entry_type == 'Object' and 'RootTemplate' in entry_data:
                root_template = entry_data['RootTemplate']
                command = f'ItemTemplateAddTo("{root_template}", CharacterGetHostCharacter(), {quantity}, 1)'
                if entry_name.startswith('SKILLBOOK_'):
                    _, school, _ = entry_name.split('_', 2)
                    if school not in school_commands:
                        school_commands[school] = []
                    school_commands[school].append(command)
                else:
                    ungrouped_commands.append(command)

    return school_commands, ungrouped_commands


# Replace 'your_folder_path_here' with the path to your folder containing text files
# Replace 'quantity_here' with the desired quantity for each command
process_files_in_folder(r'C:\Users\tungnd\Desktop\test_scripts', 3)
