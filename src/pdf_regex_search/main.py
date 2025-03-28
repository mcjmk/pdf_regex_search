#!/usr/bin/env python3
"""
PDF Regex Search - a tool to find REGEXes in PDFs
"""

import os
import re
import time

from pypdf import PdfReader
from utils import clean_text, fix_text

CONFIG = {
    "REGEX_PATTERNS": [
        r"^[0-9]{3}-[0-9]{3}-[0-9]{3}$",  # ex. phone number 123-456-789
    ],
    "PDF_FOLDER": os.path.join("pdfs", ""),
    "OVERLAP_SIZE": 10,
    "BLOCK_SIZE": 50,
}


def main():
    start_time = time.time()

    pdf_files = [
        filename
        for filename in os.listdir(CONFIG["PDF_FOLDER"])
        if filename.endswith(".pdf")
    ]
    regexes = [
        re.compile(pattern, re.IGNORECASE) for pattern in CONFIG["REGEX_PATTERNS"]
    ]
    unique_regex_matches = set()

    for pdf in pdf_files:
        try:
            with open(os.path.join(CONFIG["PDF_FOLDER"], pdf), "rb") as pdf_file_obj:
                pdfReader = PdfReader(pdf_file_obj)
                print(f"{pdf} has {len(pdfReader.pages)} pages.")
                previous_overlap = ""

            for i, page in enumerate(pdfReader.pages, start=0):
                print(f"Site: {i}", end=" ")
                page_text = fix_text(clean_text(page.extract_text()))
                blocks = [
                    page_text[j : j + CONFIG["BLOCK_SIZE"]]
                    for j in range(0, len(page_text), CONFIG["BLOCK_SIZE"])
                ]

                for j, block in enumerate(blocks, start=0):
                    print(f"block {j}: {block}")
                    found_in_block = set()
                    for regex in regexes:
                        matches = regex.findall(previous_overlap + block)
                        for match in matches:
                            unique_regex_matches.add((i, j))
                            found_in_block.add((i, j))
                    previous_overlap = block[
                        -(min(CONFIG["OVERLAP_SIZE"], len(block))) :
                    ]
        except FileNotFoundError:
            print(f"Error: Could not find file: {pdf}")

    end_time = time.time()
    sorted_matches = sorted(unique_regex_matches)
    matches_dict = {}
    for page, line in sorted_matches:
        if page in matches_dict:
            matches_dict[page].append(line)
        else:
            matches_dict[page] = [line]

    print(f"\nTotal unique regex matches found: {len(unique_regex_matches)}")
    if len(unique_regex_matches):
        for page, lines in matches_dict.items():
            lines_str = ", ".join(map(str, lines))
            print(f"Page {page}: lines {lines_str}")
    elapsed_time = end_time - start_time
    print(f"Running time: {elapsed_time} seconds.")


if __name__ == "__main__":
    main()
