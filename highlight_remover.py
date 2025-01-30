import fitz  # PyMuPDF
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import math

# not in use yet
def is_close_to_black(r, g, b, threshold=50):
    """
    Determines if a pixel is close to black within a given threshold.
    Uses the Euclidean distance formula.
    """
    return math.sqrt(r ** 2 + g ** 2 + b ** 2) <= threshold


def modify_pdf_colors(input_path, output_path):
    # Open the PDF
    doc = fitz.open(input_path)
    for page in doc:
        # Iterate through the objects on the page
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            if stream:
                # Replace yellow color with white
                # This assumes yellow is defined as (1 1 0) in RGB
                if b"1 1 0" in stream:
                    yellow_found = True
                stream = stream.replace(b"1 1 0", b"1 1 1")
                doc.update_stream(xref, stream)

    # Save the modified PDF
    doc.save(output_path)
    doc.close()


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

        print(f"Processing: {pdf_file}")
        modify_pdf_colors(input_pdf_path, output_pdf_path)
        print(f"Processed PDF saved as: {output_pdf_path}")

    print(f"All processed PDFs are saved in the folder: {processed_folder}")


if __name__ == "__main__":
    main()
