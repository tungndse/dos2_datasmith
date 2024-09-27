import re


def process_skillbooks(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    # Find all entries in the text
    entries = data.split('new entry')

    # Dictionary to group commands by school
    grouped_commands = {}
    ungrouped_commands = []

    for entry in entries:
        if not entry.strip():
            continue

        # Extract entry name
        name_match = re.search(r'\"(.*?)\"', entry)
        if name_match:
            entry_name = name_match.group(1)
        else:
            continue

        # Extract RootTemplate value
        root_template_match = re.search(r'data "RootTemplate" "(.*?)"', entry)
        if root_template_match:
            root_template = root_template_match.group(1)
        else:
            continue

        # Construct the console command
        command = f'ItemTemplateAddTo("{root_template}", CharacterGetHostCharacter(), 1, 1)'

        # Check if the entry name follows the SKILLBOOK_School_SpellName pattern
        skillbook_match = re.match(r'SKILLBOOK_([A-Za-z]+)_', entry_name)
        if skillbook_match:
            school = skillbook_match.group(1)
            if school not in grouped_commands:
                grouped_commands[school] = []
            grouped_commands[school].append(command)
        else:
            # If it doesn't match the pattern, add to ungrouped commands
            ungrouped_commands.append(command)

    # Prepare the result text
    result = ""
    for school, commands in grouped_commands.items():
        result += f"// {school.upper()}\n"
        result += "\n".join(commands) + "\n\n"

    # Add ungrouped items at the end
    if ungrouped_commands:
        result += "// UNGROUPED\n"
        result += "\n".join(ungrouped_commands) + "\n"

    # Write the result to a new file
    with open('output_commands.txt', 'w') as output_file:
        output_file.write(result)

    print("Processing complete. Check 'output_commands.txt' for results.")


# Example usage
process_skillbooks('input.txt')
