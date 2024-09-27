import os

def generate_add_skill_commands(folder_path, project_folder_path):
    """Generate CharacterAddSkill commands from skill data files with non-zero cooldown and save to project folder."""
    add_skill_commands = []

    # List all files in the specified folder with prefix 'Skill_'
    for filename in os.listdir(folder_path):
        if filename.startswith("Skill_") and filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # Open and read each skill data file
            with open(file_path, 'r') as file:
                lines = file.readlines()
                skill_name = None
                skill_type = None
                cooldown = None
                has_description = False
                has_description_ref = False

                for line in lines:
                    line = line.strip()
                    if line.startswith('new entry'):
                        # Check if all conditions are met for the previous skill entry
                        if (skill_name and skill_type == 'SkillData' and cooldown != "0" and
                            has_description and has_description_ref and
                            '_Summon' not in skill_name):  # Exclude skills with '_Summon'
                            command = f'CharacterAddSkill(CharacterGetHostCharacter(), "{skill_name}", 1)'
                            add_skill_commands.append(command)
                        # Reset for new skill entry
                        skill_name = line.split('"')[1]
                        skill_type = None
                        cooldown = None
                        has_description = False
                        has_description_ref = False
                    elif line.startswith('type'):
                        skill_type = line.split('"')[1]
                    elif line.startswith('data "Cooldown"'):
                        cooldown = line.split('"')[1]
                    elif line.startswith('data "Description"'):
                        has_description = True
                    elif line.startswith('data "DescriptionRef"'):
                        has_description_ref = True

                # Check last entry in case the file ends without a new entry
                if (skill_name and skill_type == 'SkillData' and cooldown != "0" and
                    has_description and has_description_ref and
                    '_Summon' not in skill_name):  # Exclude skills with '_Summon'
                    command = f'CharacterAddSkill(CharacterGetHostCharacter(), "{skill_name}", 1)'
                    add_skill_commands.append(command)

    # Save the commands to a file in the project folder
    output_file_path = os.path.join(project_folder_path, 'add_skills_commands.txt')
    with open(output_file_path, 'w') as output_file:
        for command in add_skill_commands:
            output_file.write(command + '\n')

    print(f"Commands saved to {output_file_path}")

# Example usage
folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop\OdinbladeGeomancerOverhaul_ffb501cc-ab6d-46de-be89-732c9e289f3e\Public\OdinbladeGeomancerOverhaul_ffb501cc-ab6d-46de-be89-732c9e289f3e\Stats\Generated\Data'  # Replace with the folder path containing Skill_*.txt files
output_folder_path = r'C:\Users\tungnd\Desktop\dos2_workshop'  # Replace with your Python project folder path
generate_add_skill_commands(folder_path, output_folder_path)
