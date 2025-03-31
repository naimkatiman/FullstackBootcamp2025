import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip install pymupdf")
    import fitz

def convert_pdf_to_image(pdf_path, output_dir="images", first_page_only=True):
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
        
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def update_readme_with_images(readme_path="README.md", image_dir="images"):
    """
    Update the README.md with links to the converted images
    """
    try:
        # Read the current README
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find PNG files in the images directory that don't end with _1.png, _2.png, etc.
        image_files = []
        for f in os.listdir(image_dir):
            if os.path.isfile(os.path.join(image_dir, f)) and f.endswith(".png"):
                # Exclude files that end with _1.png, _2.png, etc.
                if not any(f.endswith(f"_{i}.png") for i in range(1, 10)):
                    image_files.append(f)
            
        if not image_files:
            print("No converted images found in the images directory.")
            return
            
        # Create image references for each PDF
        image_markdown = "\n## PDF Documents\n\n"
        for img_file in image_files:
            name = Path(img_file).stem
            image_markdown += f"### {name}\n"
            image_markdown += f"![{name}]({image_dir}/{img_file})\n\n"
            
        # Check if the "PDF Documents" section already exists
        if "## PDF Documents" in content:
            # Replace existing section with updated content
            import re
            content = re.sub(r"## PDF Documents.*?(?=##|\Z)", image_markdown, content, flags=re.DOTALL)
        else:
            # Add new section at the end
            content += "\n" + image_markdown
            
        # Write the updated README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {readme_path} with links to converted images")
    
    except Exception as e:
        print(f"Error updating README: {e}")

if __name__ == "__main__":
    # Simple command line parsing
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert PDF files to images and update README")
    parser.add_argument("--pdf-dir", default=".", help="Directory containing PDF files")
    parser.add_argument("--output-dir", default="images", help="Directory to save images")
    parser.add_argument("--all-pages", action="store_true", help="Convert all pages, not just the first")
    parser.add_argument("--update-readme", action="store_true", help="Update README.md with image links")
    
    args = parser.parse_args()
    
    # Find PDF files
    pdf_files = [f for f in os.listdir(args.pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {args.pdf_dir}")
        sys.exit(1)
        
    print(f"Found {len(pdf_files)} PDF files")
    
    # Convert each PDF to image
    for pdf_file in pdf_files:
        pdf_path = os.path.join(args.pdf_dir, pdf_file)
        convert_pdf_to_image(
            pdf_path, 
            args.output_dir, 
            not args.all_pages
        )
    
    # Update README if requested
    if args.update_readme:
        update_readme_with_images("README.md", args.output_dir) 