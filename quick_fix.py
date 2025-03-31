import os

def fix_linux_readme():
    """Fix the Linux Tutorial README file specifically"""
    readme_path = os.path.join("Linux Tutorial", "README.md")
    
    # Create the corrected content
    content = """# Linux tutorial


## PDF Documents

### Linux Slides
![Linux Slides](images/Linux-Slides.png)

### Linux
![Linux](images/linux.png)

"""
    
    # Write to the file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed Linux Tutorial README.md")

if __name__ == "__main__":
    fix_linux_readme() 