import fitz  # PyMuPDF
from PIL import Image
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
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

def slow_program(pdf_files, folder, processed_folder):
    """Program 1: Converts PDFs to images, processes them, and re-creates new PDFs."""


    for pdf_file in pdf_files:
        input_pdf_path = os.path.join(folder, pdf_file)
        output_pdf_path = os.path.join(processed_folder, f"processed_{pdf_file}")
        output_image_folder = os.path.join(folder, f"temp_images_{os.path.splitext(pdf_file)[0]}")

        print(f"Processing: {pdf_file}")

        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        try:
            print("  Converting PDF to images...")
            images = convert_pdf_to_images(input_pdf_path, output_image_folder)
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

    print(f"All processed PDFs are saved in the folder: {processed_folder}")


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


def fast_program(pdf_files, folder, processed_folder):
    """Program 2 execution: Modifies PDF colors."""

    for pdf_file in pdf_files:
        input_pdf_path = os.path.join(folder, pdf_file)
        output_pdf_path = os.path.join(processed_folder, f"processed_{pdf_file}")
        print(f"Processing: {pdf_file}")
        modify_pdf_colors(input_pdf_path, output_pdf_path)
        print(f"Processed PDF saved as: {output_pdf_path}")

    print(f"All processed PDFs are saved in the folder: {processed_folder}")


def main():
    """Main function to select which program to run."""
    root = Tk()
    root.withdraw()
    print("Please choose a folder containing PDF files.")
    folder = askdirectory(title="Select Folder Containing PDFs")

    if not folder:
        print("No folder selected. Exiting...")
        return

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the selected folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    processed_folder = os.path.join(folder, "processed_PDFs")
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    print("Choose which program to run:")
    print("  'f' - Faster Program: Modify PDF colors.")
    print("  's' - Slower Program: Process PDFs page-by-page with image processing.")
    choice = input("Enter your choice ('f' or 's'): ").strip().lower()

    if choice == 'f':
        fast_program(pdf_files, folder, processed_folder)
    elif choice == 's':
        slow_program(pdf_files, folder, processed_folder)
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()