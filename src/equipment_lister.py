import os
import xml.etree.ElementTree as ET


def parse_lsx_file(file_path):
    """Parse the LSX file to extract Name, RootTemplate, and Description."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    item_data = {}

    # Extract data from the LSX file
    for node in root.findall(".//node[@id='GameObjects']"):
        attributes = {attr.get('id'): attr.get('value') for attr in node.findall('attribute')}
        item_data['Name'] = attributes.get('Name', '')
        item_data['RootTemplate'] = attributes.get('MapKey', '')
        item_data['Description'] = attributes.get('Description', '')

    return item_data


def process_files(input_folder, output_folder):
    """Process all LSX files in the input folder and categorize them as armor or weapon."""
    lsx_files = [f for f in os.listdir(input_folder) if f.endswith('.lsx')]

    armor_output = []
    weapon_output = []

    for lsx_file in lsx_files:
        file_path = os.path.join(input_folder, lsx_file)
        item_data = parse_lsx_file(file_path)
        item_name = item_data.get('Name')

        # Determine the category based on the name prefix
        if item_name.startswith('ARM_'):
            armor_output.append(item_data)
        elif item_name.startswith('WPN_'):
            weapon_output.append(item_data)
        else:
            # Skip any items without the correct prefix
            continue

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save categorized data
    with open(os.path.join(output_folder, 'armor_output.txt'), 'w') as f:
        for item in armor_output:
            f.write(f"Name: {item['Name']}\n")
            f.write(f"RootTemplate: {item['RootTemplate']}\n")
            f.write(f"Description: {item['Description']}\n\n")

    with open(os.path.join(output_folder, 'weapon_output.txt'), 'w') as f:
        for item in weapon_output:
            f.write(f"Name: {item['Name']}\n")
            f.write(f"RootTemplate: {item['RootTemplate']}\n")
            f.write(f"Description: {item['Description']}\n\n")

    print(f"Processing complete. Outputs saved to '{output_folder}'.")


# Example usage
input_folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUnique_RootTemplates\lsx'
output_folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop\BonusUnique_OutputEquipment'
process_files(input_folder_path, output_folder_path)
