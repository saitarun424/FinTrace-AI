from document_loader import load_documents
from pathlib import Path
from text_splitter import split_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"

documents = load_documents(KNOWLEDGE_BASE)

for document in documents:
    chunks = split_text(document["text"])

    print(f"\nSource: {document['source']}")
    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}:")
        print(chunk)