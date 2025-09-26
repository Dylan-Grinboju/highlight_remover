import fitz  # PyMuPDF
from PIL import Image
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
import math


def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """Converts a PDF file to PNG images."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=dpi)
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        images.append(image_path)
    doc.close()
    return images


def process_image(image_path, black_threshold=100):
    """Processes the image: converts all non-white/non-black pixels to white."""
    def is_close_to_black(r, g, b, threshold):
        return math.sqrt(r**2 + g**2 + b**2) <= threshold

    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    for y in range(image.size[1]):  
        for x in range(image.size[0]):  
            r, g, b = pixels[x, y]
            if (r, g, b) != (255, 255, 255) and not is_close_to_black(r, g, b, black_threshold):
                pixels[x, y] = (255, 255, 255)
    image.save(image_path)


def convert_images_to_pdf(images, output_pdf_path):
    """Converts PNG images to a single PDF."""
    pdf_images = [Image.open(img).convert("RGB") for img in images]
    pdf_images[0].save(output_pdf_path, save_all=True, append_images=pdf_images[1:])


def find_all_pdfs_recursive(root_folder):
    """Recursively finds all PDF files in the folder and its subfolders.
    Returns a list of tuples: (relative_path_from_root, full_path)
    """
    pdf_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, root_folder)
                pdf_files.append((relative_path, full_path))
    return pdf_files

def slow_program(pdf_files, root_folder, processed_root_folder):
    """Program 1: Converts PDFs to images, processes them, and re-creates new PDFs."""

    for relative_path, full_path in pdf_files:
        # Get the directory structure for the output
        relative_dir = os.path.dirname(relative_path)
        filename = os.path.basename(relative_path)
        
        # Create output directory structure
        output_dir = os.path.join(processed_root_folder, relative_dir) if relative_dir else processed_root_folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_pdf_path = os.path.join(output_dir, f"processed_{filename}")
        output_image_folder = os.path.join(root_folder, f"temp_images_{os.path.splitext(filename)[0]}_{hash(full_path) % 10000}")

        print(f"Processing: {relative_path}")

        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        try:
            print("  Converting PDF to images...")
            images = convert_pdf_to_images(full_path, output_image_folder)
            print("  Processing images...")
            for image in images:
                process_image(image)
            print("  Converting images back to PDF...")
            convert_images_to_pdf(images, output_pdf_path)

            print(f"  Done! Processed PDF saved as: {output_pdf_path}")
        finally:
            print("  Cleaning up temporary files...")
            for file in os.listdir(output_image_folder):
                os.remove(os.path.join(output_image_folder, file))
            os.rmdir(output_image_folder)

    print(f"All processed PDFs are saved in the folder: {processed_root_folder}")


def modify_pdf_colors(input_path, output_path):
    """Program 2: Modifies PDF colors (e.g., replaces yellow with white)."""
    doc = fitz.open(input_path)
    for page in doc:
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            if stream:
                if b"1 1 0" in stream:
                    stream = stream.replace(b"1 1 0", b"1 1 1")  # Replace yellow with white
                doc.update_stream(xref, stream)
    doc.save(output_path)
    doc.close()


def fast_program(pdf_files, root_folder, processed_root_folder):
    """Program 2 execution: Modifies PDF colors."""

    for relative_path, full_path in pdf_files:
        # Get the directory structure for the output
        relative_dir = os.path.dirname(relative_path)
        filename = os.path.basename(relative_path)
        
        # Create output directory structure
        output_dir = os.path.join(processed_root_folder, relative_dir) if relative_dir else processed_root_folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_pdf_path = os.path.join(output_dir, f"processed_{filename}")
        print(f"Processing: {relative_path}")
        modify_pdf_colors(full_path, output_pdf_path)
        print(f"Processed PDF saved as: {output_pdf_path}")

    print(f"All processed PDFs are saved in the folder: {processed_root_folder}")


def main():
    """Main function to select which program to run."""
    root = Tk()
    root.withdraw()
    
    # Ask user whether to select a file or folder
    print("What would you like to process?")
    print("  '1' - Single PDF file")
    print("  '2' - Folder (will search recursively in all subfolders)")
    selection_type = input("Enter your choice (1 or 2): ").strip()
    
    pdf_files = []
    root_folder = ""
    processed_root_folder = ""
    
    if selection_type == '1':
        # Single file selection
        print("Please select a PDF file to process.")
        pdf_file_path = askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not pdf_file_path:
            print("No file selected. Exiting...")
            return
        
        if not pdf_file_path.lower().endswith('.pdf'):
            print("Selected file is not a PDF. Exiting...")
            return
        
        # Set up single file processing
        root_folder = os.path.dirname(pdf_file_path)
        filename = os.path.basename(pdf_file_path)
        relative_path = filename  # For single file, relative path is just the filename
        pdf_files = [(relative_path, pdf_file_path)]
        
        # Create processed folder next to the original file
        processed_root_folder = os.path.join(root_folder, "processed_PDFs")
        if not os.path.exists(processed_root_folder):
            os.makedirs(processed_root_folder)
        
        print(f"Selected file: {filename}")
        
    elif selection_type == '2':
        # Folder selection (original functionality)
        print("Please choose a root folder containing PDF files (will search recursively in all subfolders).")
        root_folder = askdirectory(title="Select Root Folder Containing PDFs")

        if not root_folder:
            print("No folder selected. Exiting...")
            return

        # Recursively find all PDF files
        print("Scanning for PDF files recursively...")
        pdf_files = find_all_pdfs_recursive(root_folder)

        if not pdf_files:
            print("No PDF files found in the selected folder or its subfolders.")
            return

        print(f"Found {len(pdf_files)} PDF file(s) to process across all subfolders.")
        
        # Create processed folder in the root directory
        processed_root_folder = os.path.join(root_folder, "processed_PDFs")
        if not os.path.exists(processed_root_folder):
            os.makedirs(processed_root_folder)
    
    else:
        print("Invalid choice. Exiting...")
        return
    
    # Choose processing method
    print("\nChoose which program to run:")
    print("  'f' - Faster Program: Modify PDF colors.")
    print("  's' - Slower Program: Process PDFs page-by-page with image processing.")
    choice = input("Enter your choice ('f' or 's'): ").strip().lower()

    if choice == 'f':
        fast_program(pdf_files, root_folder, processed_root_folder)
    elif choice == 's':
        slow_program(pdf_files, root_folder, processed_root_folder)
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()