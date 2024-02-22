#! python3
# PDFRegexSearch.py - a simple script to find your REGEXes in pdfs

import PyPDF2
import re
import time
import os

pdf_folder = os.path.join('pdfs', '')
overlap_size = 10   # ADJUST sensible overlap_size
block_size = 50     # ADJUST block size


def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s,.!?;:\-\'"]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def fix_text(text):
    # ADD SUITABLE RULES HERE
    return text


if __name__ == '__main__':
    start_time = time.time()

    regex_patterns = [
        # ADD YOUR REGEXES HERE
    ]

    pdfFiles = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdfFiles.append(filename)

    regexes = [re.compile(pattern, re.IGNORECASE) for pattern in regex_patterns]
    unique_regex_matches = set()

    for pdf in pdfFiles:
        with open(pdf_folder + pdf, 'rb') as pdfFileObj:
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            print(f'{pdf} has {len(pdfReader.pages)} pages.')
            previous_overlap = ''

            for i, page in enumerate(pdfReader.pages, start=0):
                print(f"Site: {i}", end=" ")
                page_text = fix_text(clean_text(page.extract_text()))
                blocks = [page_text[j:j + block_size] for j in range(0, len(page_text), block_size)]

                for j, block in enumerate(blocks, start=0):
                    print(f"block {j}: {block}")
                    found_in_block = set()
                    for regex in regexes:
                        matches = regex.findall(previous_overlap + block)
                        for match in matches:
                            unique_regex_matches.add((i, j))
                            found_in_block.add((i, j))
                    previous_overlap = block[-(min(overlap_size, len(block))):]

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
            lines_str = ", ".join(
                map(str, lines))
            print(f"Page {page}: lines {lines_str}")
    elapsed_time = end_time - start_time
    print(f"Running time: {elapsed_time} seconds.")
