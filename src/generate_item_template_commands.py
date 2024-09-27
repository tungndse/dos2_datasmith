import os

def read_output_file(file_path):
    """Read the output file and extract RootTemplate values."""
    items = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    current_item = {}
    for line in lines:
        if line.startswith('Name: '):
            current_item['Name'] = line.split(': ', 1)[1].strip()
        elif line.startswith('RootTemplate: '):
            current_item['RootTemplate'] = line.split(': ', 1)[1].strip()
        elif line.strip() == '':
            if 'RootTemplate' in current_item:
                items.append(current_item['RootTemplate'])
            current_item = {}

    return items


def generate_item_template_add_commands(armor_file, weapon_file, output_folder, quantity):
    """Generate ItemTemplateAddTo commands from RootTemplate values."""
    armor_templates = read_output_file(armor_file)
    weapon_templates = read_output_file(weapon_file)

    # Prepare output commands
    commands = []

    for template in armor_templates:
        commands.append(f'ItemTemplateAddTo("{template}", CharacterGetHostCharacter(), {quantity}, 1);')

    for template in weapon_templates:
        commands.append(f'ItemTemplateAddTo("{template}", CharacterGetHostCharacter(), {quantity}, 1);')

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write the commands to a file
    output_file_path = os.path.join(output_folder, 'item_template_commands.txt')
    with open(output_file_path, 'w') as f:
        for command in commands:
            f.write(command + '\n')

    print(f"Command generation complete. Commands saved to '{output_file_path}'.")


# Example usage
armor_output_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUnique_OutputEquipment\armor_output.txt'
weapon_output_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUnique_OutputEquipment\weapon_output.txt'
output_folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUnique_OutputEquipment'
quantity = 1  # Set the desired quantity

generate_item_template_add_commands(armor_output_path, weapon_output_path, output_folder_path, quantity)
