# PDF Highlight Remover

This is a Python-based tool for processing PDF files. It provides two main functionalities: 
1. **Faster Program** - Modifies the colors in a PDF directly.
2. **Slower Program** - Converts PDF pages to images for pixel-level image processing before re-assembling them back into a PDF.

---

## Features

### 1. Faster Program (Modify PDF Colors)
- Replaces just yellow in the PDF with white directly using PDF streams.
- Suitable for users looking for a quick solution.

### 2. Slower Program (Page-by-Page Image Processing)
- Converts PDFs to images for detailed processing.
- Processes each page by converting non-white, non-black pixels into white based on a defined threshold.
- Reassembles processed images back into a single PDF.
- Lowers the quality of the PDF!
- Takes a lot longer.

---

## Requirements

- Python 3.6+
- Required Python libraries:
  - `PyMuPDF` (`fitz`)
  - `Pillow` (`PIL`)

Install the dependencies using:
```bash
pip install PyMuPDF Pillow
```

---

## How to Use

1. Run the script:
   ```bash
   python highlight_remover.py
   ```

2. Select a folder containing the PDF files to process when prompted.

3. Choose the program to run:
   - **Faster Program**: Enter `f` and press Enter.
   - **Slower Program**: Enter `s` and press Enter.

4. The processed files will be saved in a new folder named `processed_PDFs` within the selected folder.

---

## Temporary Files

The **Slower Program** creates temporary image files during processing. These files are automatically cleaned up once processing is complete.

---

## File Structure Example

### Input
```plaintext
/path/to/folder/
    example1.pdf
    example2.pdf
```

### Output
```plaintext
/path/to/folder/
    example1.pdf
    example2.pdf
    processed_PDFs/
        processed_example1.pdf
        processed_example2.pdf
```

---

## Disclaimers

1. **Not for Sensitive Documents**: This software is a utility tool designed for general-purpose PDF processing. Avoid using it with confidential or sensitive documents unless you have reviewed the code and verified its suitability for your use case.

2. **No Warranty**: The software is provided "as is," without warranty of any kind, either expressed or implied. Use this tool at your own risk. The creators are not responsible for any unintended consequences, including but not limited to damage to files, data loss, or interruptions in workflow.

3. **Processing Limitations**: The tool may not work correctly for all types of PDFs, especially those containing complex formatting, embedded artifacts, or encrypted files. Ensure to test the program on sample files before large-scale usage.
