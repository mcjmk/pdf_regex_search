# PDFRegexSearch 
A simple Python script to search for content within PDF files using regular expressions. 

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage
1. Put your PDF files in the `pdfs` folder
2. Edit regex patterns in `src/pdf_regex_search/main.py`
3. Run the script:
   ```bash
   python -m pdf_regex_search.main
   ```

## Future Plans:
[] Add CLI
[] Add GUI 
[] Add tests
[] Add exporting results to files (txt, CSV, JSON, etc.)
