from pathlib import Path
from typing import List

from src.utils.dataclasses import Document


def load_documents(config: dict) -> List[Document]:
    """
    Discover PDF files and wrap them as Document objects.
    """
    pdf_dir = Path(config["paths"]["data"]["raw_pdfs"])

    if not pdf_dir.exists():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    documents: List[Document] = []

    for idx, pdf_path in enumerate(sorted(pdf_dir.glob("*.pdf"))):
        doc = Document(
            doc_id=f"doc_{idx}",
            source_path=str(pdf_path),
            title=None,
            sections={}
        )
        documents.append(doc)

    return documents
