from pathlib import Path

def load_documents(folder_path):
    documents = []


    folder = Path(folder_path)

    for file_path in folder.rglob("*.txt"):

        text = file_path.read_text(encoding="utf-8")

        # Extract metadata from the document header.
        metadata = {}

        for line in text.splitlines():

            if not line.strip():
                break

            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip()

        documents.append({
            "text": text,
            "source": file_path.name,
            "path": str(file_path),
            "company": metadata.get(
                "company",
                file_path.parent.name
            ),
            "reporting_period": metadata.get(
                "reporting_period",
                "Not specified"
            ),
            "document_type": metadata.get(
                "document_type",
                "Not specified"
            ),
            "publication_date": metadata.get(
                "publication_date",
                "Not specified"
            ),
            "source_url": metadata.get(
                "source_url",
                "Not provided"
            )
        })

    return documents

