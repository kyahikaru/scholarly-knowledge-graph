import requests
import xml.etree.ElementTree as ET
from pathlib import Path

# search query for NLP papers
QUERY = "natural language processing"
MAX_RESULTS = 10

# arXiv API
url = f"http://export.arxiv.org/api/query?search_query=all:{QUERY}&start=0&max_results={MAX_RESULTS}"

response = requests.get(url)
root = ET.fromstring(response.text)

# output directory
output_dir = Path("data/raw_pdfs")
output_dir.mkdir(parents=True, exist_ok=True)

papers = root.findall("{http://www.w3.org/2005/Atom}entry")

print(f"Found {len(papers)} papers. Downloading PDFs...")

for i, paper in enumerate(papers):
    pdf_link = None

    for link in paper.findall("{http://www.w3.org/2005/Atom}link"):
        if link.attrib.get("title") == "pdf":
            pdf_link = link.attrib["href"]

    if pdf_link:
        pdf_url = pdf_link + ".pdf"
        file_path = output_dir / f"paper_{i+1}.pdf"

        print(f"Downloading {pdf_url}")

        r = requests.get(pdf_url)
        with open(file_path, "wb") as f:
            f.write(r.content)

print("Download complete.")
