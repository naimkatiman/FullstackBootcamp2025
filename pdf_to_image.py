import os
import sys
from pathlib import Path
try:
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError:
    print("Required packages not installed. Installing now...")
    os.system("pip install pdf2image pillow")
    from pdf2image import convert_from_path
    from PIL import Image

def convert_pdf_to_image(pdf_path, output_dir="images", dpi=200, fmt="png", first_page_only=True):
    """
    Convert a PDF file to image(s)
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the images
        dpi: DPI for the output image
        fmt: Format of the output image (png, jpg, etc.)
        first_page_only: If True, only convert the first page
    """
    pdf_name = Path(pdf_path).stem
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # For Windows, you might need to specify the path to poppler
        # If poppler is installed, you can use:
        # images = convert_from_path(pdf_path, dpi=dpi, poppler_path=r"path\to\poppler\bin")
        
        # Try without poppler path first
        try:
            if first_page_only:
                images = convert_from_path(pdf_path, dpi=dpi, first_page=0, last_page=1)
            else:
                images = convert_from_path(pdf_path, dpi=dpi)
        except Exception as e:
            print(f"Error: {e}")
            print("If you're on Windows, you need to install poppler.")
            print("Download from: https://github.com/oschwartz10612/poppler-windows/releases")
            print("Extract it and add the bin directory to your PATH or specify the path in the script.")
            print("\nAlternatively, let's try a different approach...")
            
            # Fallback method using matplotlib
            try:
                import matplotlib.pyplot as plt
                import matplotlib.image as mpimg
                from matplotlib.backends.backend_pdf import PdfPages
                
                pdf = PdfPages(pdf_path)
                fig = plt.figure(figsize=(8.27, 11.69))  # A4 size in inches
                
                # Just extract the first page if first_page_only is True
                if first_page_only:
                    page_count = 1
                else:
                    page_count = len(pdf.pages)
                
                for i in range(page_count):
                    pdf_page = pdf.pages[i]
                    plt.figure(figsize=(8.27, 11.69))
                    plt.imshow(mpimg.imread(pdf_page))
                    plt.axis('off')
                    plt.tight_layout()
                    
                    output_path = os.path.join(output_dir, f"{pdf_name}_{i+1}.{fmt}")
                    plt.savefig(output_path, format=fmt, dpi=dpi)
                    plt.close()
                    
                    if i == 0:
                        # Also save first page with original filename for convenience
                        output_path = os.path.join(output_dir, f"{pdf_name}.{fmt}")
                        plt.figure(figsize=(8.27, 11.69))
                        plt.imshow(mpimg.imread(pdf.pages[0]))
                        plt.axis('off')
                        plt.tight_layout()
                        plt.savefig(output_path, format=fmt, dpi=dpi)
                        plt.close()
                
                pdf.close()
                print(f"Converted {pdf_path} to {output_dir}/{pdf_name}.{fmt}")
                return
            except ImportError:
                print("Could not import matplotlib. Please install it with: pip install matplotlib")
                return
            except Exception as e:
                print(f"Fallback method failed too: {e}")
                return
        
        # Save the images
        for i, image in enumerate(images):
            output_path = os.path.join(output_dir, f"{pdf_name}_{i+1}.{fmt}")
            image.save(output_path, fmt.upper())
            
            # Also save first page with original filename for convenience
            if i == 0:
                output_path = os.path.join(output_dir, f"{pdf_name}.{fmt}")
                image.save(output_path, fmt.upper())
                
        print(f"Converted {pdf_path} to {output_dir}/{pdf_name}.{fmt}")
        
        if first_page_only:
            print("Only converted the first page. Use --all-pages to convert all pages.")
    
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
            
        # Find PDF files that have been converted to images
        image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and not f.endswith("_1.png")]
            
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
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert PDF files to images and update README")
    parser.add_argument("--pdf-dir", default=".", help="Directory containing PDF files")
    parser.add_argument("--output-dir", default="images", help="Directory to save images")
    parser.add_argument("--dpi", type=int, default=200, help="DPI for output images")
    parser.add_argument("--format", default="png", help="Format for output images (png, jpg)")
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
            args.dpi, 
            args.format, 
            not args.all_pages
        )
    
    # Update README if requested
    if args.update_readme:
        update_readme_with_images("README.md", args.output_dir) 