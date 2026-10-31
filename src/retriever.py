from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

COLLECTION_NAME = "financial_documents"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


COMPANY_ALIASES = {
    "NVIDIA Corporation": ["nvidia"],
    "Microsoft Corporation": ["microsoft"],
    "Tata Consultancy Services Limited": [
        "tcs",
        "tata consultancy services"
    ],
    "Jio Platforms Limited": [
        "jio platforms",
        "jio"
    ]
}


embedding_model = SentenceTransformer(EMBEDDING_MODEL)

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


def detect_companies(question):

    detected = []

    question = question.lower()

    for company, aliases in COMPANY_ALIASES.items():

        if any(alias in question for alias in aliases):
            detected.append(company)

    return detected


def retrieve_documents(question, top_k=10, company=None):

    if not question or not question.strip():
        return []

    if collection.count() == 0:
        return []

    query_embedding = embedding_model.encode(
        question.strip()
    ).tolist()

    companies = (
        [company]
        if company
        else detect_companies(question)
    )

    query_groups = companies if companies else [None]

    results = []
    seen = set()

    for company_name in query_groups:

        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": min(top_k, collection.count()),
            "include": [
                "documents",
                "metadatas",
                "distances"
            ]
        }

        if company_name:
            query_args["where"] = {
                "company": company_name
            }

        response = collection.query(**query_args)

        texts = response["documents"][0]
        metadatas = response["metadatas"][0]

        for text, metadata in zip(texts, metadatas):

            source = metadata.get("source", "Unknown")

            key = (source, text)

            if key in seen:
                continue

            seen.add(key)

            results.append({
                "text": text,
                "company": metadata.get("company"),
                "source": source,
                "reporting_period": metadata.get(
                    "reporting_period"
                ),
                "source_url": metadata.get("source_url")
            })

    return results