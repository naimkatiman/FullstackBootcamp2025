import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip install pymupdf")
    import fitz

def convert_pdf_to_image(pdf_path, output_dir="images"):
    """
    Convert a PDF file to PNG image using PyMuPDF (fitz)
    """
    pdf_name = Path(pdf_path).stem
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Get the first page
        page = doc[0]
        
        # Render page to an image with higher resolution
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
        
        # Save the image
        output_path = os.path.join(output_dir, f"{pdf_name}.png")
        pix.save(output_path)
        
        print(f"Successfully converted {pdf_path} to {output_path}")
        
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

if __name__ == "__main__":
    # Convert the specific PDF
    pdf_path = "images/system-design.pdf"
    convert_pdf_to_image(pdf_path, "images") 