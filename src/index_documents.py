from pathlib import Path
import re

from retriever import (
    collection,
    embedding_model,
    PROJECT_ROOT
)


KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150


def read_header_value(text, key):

    match = re.search(
        rf"^{re.escape(key)}:\s*(.+)$",
        text,
        re.IGNORECASE | re.MULTILINE
    )

    return match.group(1).strip() if match else ""


def split_text(text):

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + CHUNK_SIZE, len(text))

        if end < len(text):

            boundary = text.rfind("\n", start, end)

            if boundary > start + int(CHUNK_SIZE * 0.6):
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - CHUNK_OVERLAP, start + 1)

    return chunks


def main():

    if not KNOWLEDGE_BASE.exists():
        raise FileNotFoundError("Knowledge base folder not found.")

    text_files = sorted(
        KNOWLEDGE_BASE.rglob("*.txt")
    )

    records = []

    for path in text_files:

        text = path.read_text(
            encoding="utf-8",
            errors="replace"
        ).strip()

        if not text:
            continue

        company = read_header_value(text, "COMPANY")

        period = read_header_value(
            text,
            "REPORTING_PERIOD"
        )

        source_url = read_header_value(
            text,
            "SOURCE_URL"
        )

        if not company:
            continue

        chunks = split_text(text)

        for index, chunk in enumerate(chunks):

            records.append({
                "id": f"{path.relative_to(KNOWLEDGE_BASE).as_posix()}_{index}",
                "text": chunk,
                "metadata": {
                    "company": company,
                    "source": path.name,
                    "reporting_period": period or "Not specified",
                    "source_url": source_url or "Not available"
                }
            })

    if not records:
        raise RuntimeError(
            "No valid knowledge-base documents found."
        )

    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    batch_size = 64

    for start in range(0, len(records), batch_size):

        batch = records[start:start + batch_size]

        texts = [
            item["text"]
            for item in batch
        ]

        embeddings = embedding_model.encode(
            texts,
            show_progress_bar=False
        ).tolist()

        collection.upsert(
            ids=[
                item["id"]
                for item in batch
            ],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                item["metadata"]
                for item in batch
            ]
        )

    print("Knowledge base indexing completed.")
    print("Total indexed chunks:", len(records))


if __name__ == "__main__":

    main()