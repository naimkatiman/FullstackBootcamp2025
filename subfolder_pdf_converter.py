import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip install pymupdf")
    import fitz

def convert_pdf_to_image(pdf_path, output_dir, first_page_only=True):
    """
    Convert a PDF file to PNG images using PyMuPDF (fitz)
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the images
        first_page_only: If True, only convert the first page
    """
    pdf_name = Path(pdf_path).stem
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Determine how many pages to convert
        if first_page_only:
            pages_to_convert = [0]  # Just the first page (0-indexed)
        else:
            pages_to_convert = range(len(doc))
            
        for page_num in pages_to_convert:
            # Get the page
            page = doc[page_num]
            
            # Render page to an image with higher resolution
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
            
            # Save the image
            if page_num == 0:
                # Save first page with the PDF name
                output_path = os.path.join(output_dir, f"{pdf_name}.png")
                pix.save(output_path)
                
            # Also save with page number
            output_path = os.path.join(output_dir, f"{pdf_name}_{page_num+1}.png")
            pix.save(output_path)
            
        print(f"Successfully converted {pdf_path} to {output_dir}/{pdf_name}.png")
        return f"{pdf_name}.png"  # Return the base filename
        
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return None

def create_or_update_readme(folder_path, image_files):
    """
    Create or update README.md in the specified folder
    
    Args:
        folder_path: Path to the folder
        image_files: List of tuples (image_filename, original_pdf_name)
    """
    readme_path = os.path.join(folder_path, "README.md")
    
    # Check if README.md exists
    if os.path.exists(readme_path):
        # Read existing content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Create new README with folder name as title
        folder_name = os.path.basename(folder_path)
        content = f"# {folder_name.capitalize()}\n\n"
    
    # Create images section
    images_section = "\n## PDF Documents\n\n"
    for img_file, pdf_name in image_files:
        # Use PDF name as the title, but clean it up
        name = pdf_name.replace('_', ' ').replace('-', ' ').title()
        images_section += f"### {name}\n"
        # Use relative path for images within the same folder
        images_section += f"![{name}](images/{img_file})\n\n"
    
    # Check if PDF Documents section already exists
    if "## PDF Documents" in content:
        # Replace existing section
        import re
        content = re.sub(r"## PDF Documents.*?(?=##|\Z)", images_section, content, flags=re.DOTALL)
    else:
        # Add new section
        content += images_section
    
    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {readme_path}")

def process_folder(folder_path, all_pages=False):
    """
    Process all PDF files in a folder and update its README.md
    
    Args:
        folder_path: Path to the folder
        all_pages: Whether to convert all pages or just the first
    """
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    
    # Create images subfolder
    images_dir = os.path.join(folder_path, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Find PDF files
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files in {folder_path}")
    
    # Convert each PDF and collect image references
    image_files = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        img_file = convert_pdf_to_image(
            pdf_path, 
            images_dir, 
            not all_pages
        )
        if img_file:
            image_files.append((img_file, Path(pdf_file).stem))
    
    # Update README.md
    if image_files:
        create_or_update_readme(folder_path, image_files)

if __name__ == "__main__":
    # Define the subfolders to process
    subfolders = [
        "Docker", 
        "AWS", 
        "Linux Tutorial", 
        "MongoDB", 
        "PHP", 
        "Python", 
        "React", 
        "Redis", 
        "Javascript & Typescript"
    ]
    
    # Process each subfolder
    for folder in subfolders:
        print(f"\nProcessing {folder}...")
        process_folder(folder)
    
    print("\nAll folders processed successfully!") 