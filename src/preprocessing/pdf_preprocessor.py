from typing import List
from pathlib import Path

import pdfplumber

from src.utils.dataclasses import Document


def preprocess_documents(documents: List[Document], config: dict) -> List[Document]:
    """
    Extract raw text from PDFs and populate Document.sections.
    """
    keep_sections = set(
        s.lower() for s in config["preprocessing"]["sections"]["keep"]
    )

    processed_docs: List[Document] = []

    for doc in documents:
        pdf_path = Path(doc.source_path)

        if not pdf_path.exists():
            continue

        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

        # VERY rough sectioning (MWP-level)
        sections = {}
        lower_text = full_text.lower()

        for section in keep_sections:
            if section in lower_text:
                sections[section] = full_text

        doc.sections = sections
        processed_docs.append(doc)

    return processed_docs
