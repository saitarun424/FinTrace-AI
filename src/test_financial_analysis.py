from retriever import retrieve_documents
from financial_analysis import analyze_companies


question = (
    "Compare the revenue performance of Microsoft, NVIDIA, "
    "TCS, and Jio Platforms."
)

print("\nRetrieving financial documents...")

# Retrieve more chunks to improve the chance of
# including both current and previous-year revenue.
documents = retrieve_documents(
    question,
    top_k=10
)

print("Retrieved document chunks:", len(documents))

results = analyze_companies(documents)

print("\n" + "=" * 60)
print("          FINTRACE AI - FINANCIAL ANALYSIS")
print("=" * 60)

if not results:

    print("\nNo financial information found.")

else:

    for result in results:

        print("\nCompany:", result["company"])
        print("Current Period:", result["period"])

        print(
            "Current Revenue:",
            result["current_revenue"],
            result["unit"]
        )

        if result["previous_revenue"] is not None:

            print(
                "Previous Period:",
                result["previous_period"]
            )

            print(
                "Previous Revenue:",
                result["previous_revenue"],
                result["unit"]
            )

            print(
                "Revenue Growth:",
                result["growth_percentage"],
                "%"
            )

        else:

            print("Previous Revenue: Not found in retrieved text")
            print("Revenue Growth: Not calculated")

        print("Source:", result["source"])

        print("-" * 60)

print("\nFinancial analysis completed.")