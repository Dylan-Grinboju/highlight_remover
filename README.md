# Remove highlight from PDFs

# PDF Color Modifier Tool

This tool processes PDF files in a selected folder and replaces yellow colors with white. The modified PDFs are saved in a new folder called `processed_PDFs`.

## Requirements
- Python 3.x
- PyMuPDF library (`pip install pymupdf`)

## How to Use
1. Run the script:
   ```
   python highlight_remover.py
   ```
2. Select a folder with PDF files when prompted.
3. The processed PDFs will be saved in a subfolder named `processed_PDFs` inside the selected folder.

That's it! 🎉

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

## Notes
- The script replaces yellow (`1 1 0`) with white (`1 1 1`) in the PDF. It will not work (yet) for other shades of yellow.
- Only works with accessible and non-password-protected PDFs.

## Disclaimers

1. **Not for Sensitive Documents**: This software is a utility tool designed for general-purpose PDF processing. Avoid using it with confidential or sensitive documents unless you have reviewed the code and verified its suitability for your use case.

2. **No Warranty**: The software is provided "as is," without warranty of any kind, either expressed or implied. Use this tool at your own risk. The creators are not responsible for any unintended consequences, including but not limited to damage to files, data loss, or interruptions in workflow.

3. **Processing Limitations**: The tool may not work correctly for all types of PDFs, especially those containing complex formatting, embedded artifacts, or encrypted files. Ensure to test the program on sample files before large-scale usage.
