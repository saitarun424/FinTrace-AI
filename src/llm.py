import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from retriever import retrieve_documents
from financial_analysis import analyze_companies


# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# OpenRouter configuration
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:7861",
        "X-Title": "FinTrace AI"
    }
)

MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free"


def generate_answer(question):

    try:
        # Retrieve relevant financial documents
        documents = retrieve_documents(
            question,
            top_k=10
        )

        if not documents:
            return "No relevant financial documents found."

        # Extract financial information
        analysis = analyze_companies(documents)

        # Prepare document context
        context_parts = []

        for doc in documents:

            if isinstance(doc, dict):
                text = doc.get(
                    "text",
                    doc.get("page_content", "")
                )
            else:
                text = getattr(
                    doc,
                    "page_content",
                    str(doc)
                )

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        # Prepare calculated financial results
        financial_results = []

        for item in analysis:

            financial_results.append(
                f"""
Company: {item['company']}
Current Period: {item['period']}
Current Revenue: {item['current_revenue']} {item['unit']}
Previous Period: {item['previous_period']}
Previous Revenue: {item['previous_revenue']} {item['unit']}
Calculated Growth: {item['growth_percentage']}%
Source: {item['source']}
"""
            )

        analysis_text = "\n".join(financial_results)

        # Create prompt
        prompt = f"""
You are FinTrace AI, a financial research assistant.

Answer the user's question using ONLY the supplied
financial documents and calculated financial results.

IMPORTANT RULES:

1. Do not invent financial figures.
2. Preserve reporting periods and currencies.
3. Distinguish revenue from profit and other metrics.
4. Mention the company name.
5. Include source references.
6. If information is missing, clearly say so.
7. Explain that calculated growth is based on the
   extracted revenue figures.
8. Do not compare different currencies as if they
   were the same.
9. Do not claim independent verification unless
   the original report has actually been checked.

USER QUESTION:
{question}

CALCULATED FINANCIAL RESULTS:
{analysis_text}

RETRIEVED KNOWLEDGE BASE:
{context}

Prepare a clear, structured financial analysis.
"""

        # Send request to OpenRouter
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as e:

        print("FinTrace AI Error:", str(e))

        return (
            "Unable to generate the financial analysis. "
            "Please check your OpenRouter API configuration "
            "and model availability.\n\n"
            f"Error: {str(e)}"
        )