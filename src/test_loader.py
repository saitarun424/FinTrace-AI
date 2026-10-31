from pathlib import Path
from document_loader import load_documents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"

documents = load_documents(KNOWLEDGE_BASE)

print(f"Documents loaded: {len(documents)}")

for document in documents:
    print("\n-----------------------------")
    print("Source:", document["source"])
    print("Company:", document["company"])
    print("Reporting Period:", document["reporting_period"])
    print("Document Type:", document["document_type"])
    print("Publication Date:", document["publication_date"])
    print("Source URL:", document["source_url"])
    print("-----------------------------")
