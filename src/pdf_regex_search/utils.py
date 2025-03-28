import re


def clean_text(text):
    """Clean text by removing special characters and extra whitespace"""
    text = re.sub(r'[^a-zA-Z0-9\s,.!?;:\-\'"]', "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def fix_text(text):
    return text.strip()
