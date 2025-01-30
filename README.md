# Remove highlight from PDFs

This program performs a three-step process on PDF files in a selected folder:
1. Converts each page of a PDF file into PNG images.
2. Processes the images by converting non-white/black pixels to white.
3. Converts the processed images back into a single PDF file.

All processed PDFs will be saved in a `processed_PDFs` folder within the selected folder.

---

## Requirements

Make sure the following Python libraries are installed in your environment:

1. [PyMuPDF](https://pymupdf.readthedocs.io/): For reading and processing PDFs.
   ```bash
   pip install pymupdf
   ```

2. [Pillow](https://pillow.readthedocs.io/): For image processing.
   ```bash
   pip install pillow
   ```

3. [Tkinter](https://docs.python.org/3/library/tkinter.html): For folder selection GUI (usually included in Python's standard library).

---

## How to Use

1. **Run the Program**:
   Execute the script. You can use the command:
   ```bash
   python highlight_remover.py
   ```

2. **Select Folder**:
   A folder selection dialog will appear. Choose a folder containing the PDF files you want to process.

3. **Processing**:
   - The script will process each PDF file in the folder.
   - For each PDF:
     - It saves the extracted pages as temporary images in a subfolder (e.g., `temp_images_filename`).
     - Processes the images (changes non-white/black pixels to white).
     - Combines the processed images into a new PDF and saves it in a `processed_PDFs` folder.

4. **Output**:
   - Processed PDFs are saved as `processed_filename.pdf` in the `processed_PDFs` subfolder of the original folder.
   - Temporary images are deleted after processing is complete.

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

Temporary image folders like `temp_images_example1` will be created during the process but removed after the PDF is generated.

---

## Notes

- **Error Handling**: If no folder or PDFs are found, the script will prompt and safely exit without running any operations.
- **Ensure Write Permissions**: Make sure the script has write access to the target folder for saving the `processed_PDFs` and any intermediate files.
- **Large Input Files**: For PDFs with many pages, processing may take longer, depending on system capabilities.

---

## Disclaimers

1. **Not for Sensitive Documents**: This software is a utility tool designed for general-purpose PDF processing. Avoid using it with confidential or sensitive documents unless you have reviewed the code and verified its suitability for your use case.

2. **No Warranty**: The software is provided "as is," without warranty of any kind, either expressed or implied. Use this tool at your own risk. The creators are not responsible for any unintended consequences, including but not limited to damage to files, data loss, or interruptions in workflow.

3. **Processing Limitations**: The tool may not work correctly for all types of PDFs, especially those containing complex formatting, embedded artifacts, or encrypted files. Ensure to test the program on sample files before large-scale usage.
