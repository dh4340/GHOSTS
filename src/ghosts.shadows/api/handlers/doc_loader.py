import json
import os

from docx import Document
from PyPDF2 import PdfReader


def load_document(file_path):
    if file_path.endswith(".pdf"):
        return "".join([page.extract_text() for page in PdfReader(file_path).pages])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return json.dumps(json.load(f))
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            return f.read()
    else:
        return ""


def load_documents_from_directories(docs_dirs):
    documents = []
    for docs_dir in docs_dirs:
        if os.path.exists(docs_dir) and os.listdir(docs_dir):
            for file in os.listdir(docs_dir):
                file_path = os.path.join(docs_dir, file)
                if os.path.isfile(file_path):
                    documents.append(load_document(file_path))
    return documents


def split_documents_into_chunks(documents, chunk_size=250):
    chunks = []
    for doc in documents:
        chunks.extend([doc[i : i + chunk_size] for i in range(0, len(doc), chunk_size)])
    return chunks
