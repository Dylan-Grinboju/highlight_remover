import fitz  # PyMuPDF
from PIL import Image
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


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


def process_image(image_path):
    """Processes the image: converts non-white/black pixels to white."""
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()  # Load pixel-level access to the image
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b = pixels[x, y]
            # Check if the pixel is not white or black
            if (r, g, b) != (255, 255, 255) and (r, g, b) != (0, 0, 0):
                pixels[x, y] = (255, 255, 255)  # Change to white
    image.save(image_path)


def convert_images_to_pdf(images, output_pdf_path):
    """Converts PNG images to a single PDF."""
    pdf_images = [Image.open(img).convert("RGB") for img in images]
    pdf_images[0].save(output_pdf_path, save_all=True, append_images=pdf_images[1:])


def main():
    # Hide the root Tkinter window so only the file dialog shows
    root = Tk()
    root.withdraw()
    
    # Ask the user to select a folder
    print("Please choose a folder containing PDF files.")
    folder = askdirectory(title="Select Folder Containing PDFs")
    
    # Display an error and exit if the user cancels or no folder is selected
    if not folder:
        print("No folder selected. Exiting...")
        return

    # Get a list of PDF files in the selected folder
    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the selected folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process.")

    # Create a subfolder for processed PDFs
    processed_folder = os.path.join(folder, "processed_PDFs")
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # Process each PDF file
    for pdf_file in pdf_files:
        input_pdf_path = os.path.join(folder, pdf_file)
        output_pdf_path = os.path.join(processed_folder, f"processed_{pdf_file}")
        output_image_folder = os.path.join(folder, f"temp_images_{os.path.splitext(pdf_file)[0]}")

        print(f"Processing: {pdf_file}")

        # Create a temporary folder for images
        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        try:
            # Step 1: Convert PDF to images
            print("  Converting PDF to images...")
            images = convert_pdf_to_images(input_pdf_path, output_image_folder)

            # Step 2: Process each image
            print("  Processing images...")
            for image in images:
                process_image(image)

            # Step 3: Convert processed images back to PDF
            print("  Converting images back to PDF...")
            convert_images_to_pdf(images, output_pdf_path)

            print(f"  Done! Processed PDF saved as: {output_pdf_path}")
        finally:
            # Cleanup: Delete temporary images
            print("  Cleaning up temporary files...")
            for file in os.listdir(output_image_folder):
                os.remove(os.path.join(output_image_folder, file))
            os.rmdir(output_image_folder)

    print(f"All processed PDFs are saved in the folder: {processed_folder}")


if __name__ == "__main__":
    main()