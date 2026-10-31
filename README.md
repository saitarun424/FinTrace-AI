# FinTrace AI

FinTrace AI is a simple RAG-based financial research assistant.

It allows users to ask questions about company financial reports
and receive answers grounded in a financial knowledge base.

## Technology Stack

- Python
- Gemini 2.5 Flash
- Retrieval-Augmented Generation (RAG)
- ChromaDB
- Sentence Transformers
- Gradio

## Supported Companies

- Microsoft
- NVIDIA
- Tata Consultancy Services
- Jio Platforms

## Features

- Financial document retrieval
- Natural language question answering
- Revenue extraction
- Python-based revenue growth calculations
- Source references
- Simple Gradio interface

## Application Workflow

User Question
    |
    v
Gradio Interface
    |
    v
Document Retrieval
    |
    v
ChromaDB
    |
    v
Financial Knowledge Base
    |
    v
Python Financial Analysis
    |
    v
Gemini LLM
    |
    v
Generated Answer

## Installation

Install dependencies:

pip install -r requirements.txt

Configure your Gemini API key in the .env file.

## Index Knowledge Base

python src/index_documents.py

## Run Application

python src/app.py

Open:

http://127.0.0.1:7861

## Limitations

Answers depend on the documents available in the knowledge base.
Financial figures should be verified against original company reports.