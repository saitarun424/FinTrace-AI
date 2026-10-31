import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="./data/chroma_db"
)


# Create collection
collection = client.get_or_create_collection(
    name="financial_documents",
    metadata={"hnsw:space": "cosine"}
)


# Convert text into numerical vectors
def generate_embedding(text):

    embedding = embedding_model.encode(text)

    return embedding.tolist()


# Store chunks and metadata in ChromaDB
def store_chunks(chunks, metadata):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"{metadata['company']}_{metadata['source']}_{index}"
        )

        documents.append(chunk)

        embeddings.append(
            generate_embedding(chunk)
        )

        metadatas.append({
            "company": metadata["company"],
            "source": metadata["source"],
            "reporting_period": metadata["reporting_period"],
            "document_type": metadata["document_type"],
            "publication_date": metadata["publication_date"],
            "source_url": metadata["source_url"],
            "chunk_index": index
        })

    if ids:

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    print(f"Stored {len(ids)} chunks for {metadata['company']}.")