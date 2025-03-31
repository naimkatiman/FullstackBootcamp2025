import os
import re
from pathlib import Path

def fix_readme_duplicates(folder_path):
    """
    Fix duplicate entries in README.md files
    """
    readme_path = os.path.join(folder_path, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"README.md not found in {folder_path}")
        return
    
    # Read the content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the PDF Documents section
    if "## PDF Documents" not in content:
        print(f"No PDF Documents section found in {readme_path}")
        return
    
    # Split the content to get parts before and after the PDF Documents section
    parts = content.split("## PDF Documents")
    before_section = parts[0]
    after_match = re.search(r"(?:##|\Z)(.*?)$", parts[1], re.DOTALL)
    after_section = after_match.group(1) if after_match else ""
    
    # Extract image entries from the PDF Documents section
    section = parts[1].split("##")[0] if "##" in parts[1] else parts[1]
    image_entries = re.findall(r"### (.*?)\n!\[(.*?)\]\((.*?)\)", section, re.DOTALL)
    
    # Keep track of unique entries based on the image path
    unique_entries = {}
    for title, alt, path in image_entries:
        if path not in unique_entries:
            unique_entries[path] = (title, alt)
    
    # Rebuild the section
    new_section = "## PDF Documents\n\n"
    for path, (title, alt) in unique_entries.items():
        new_section += f"### {title}\n![{alt}]({path})\n\n"
    
    # Reassemble the content
    new_content = before_section + new_section
    if "##" in parts[1]:
        new_content += "##" + after_section
    
    # Write back to the file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed duplicates in {readme_path}")

if __name__ == "__main__":
    # Define the subfolders to process
    subfolders = [
        "Docker", 
        "AWS", 
        "Linux Tutorial",  # This had duplicates
        "MongoDB", 
        "PHP", 
        "Python", 
        "React", 
        "Redis", 
        "Javascript & Typescript"
    ]
    
    # Process each subfolder
    for folder in subfolders:
        print(f"Checking {folder}...")
        fix_readme_duplicates(folder)
    
    print("All README files checked and fixed!") 