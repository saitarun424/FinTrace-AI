import re
from collections import defaultdict


def get_document_data(doc):
    """Support dictionary and LangChain document formats."""

    if isinstance(doc, dict):
        metadata = doc.get("metadata", doc)

        text = (
            doc.get("text")
            or doc.get("page_content")
            or doc.get("content")
            or ""
        )

        return text, metadata

    metadata = getattr(doc, "metadata", {})
    text = getattr(doc, "page_content", str(doc))

    return text, metadata


def extract_revenue_records(text):

    period_pattern = (
        r"(Q[1-4]\s+FY\d{4}|FY\d{4}-\d{2})"
    )

    currency_pattern = r"(US\$|USD|INR|₹|â‚¹|\$)?"

    amount_pattern = r"([\d,]+(?:\.\d+)?)"

    unit_pattern = r"(billion|million|crore)"

    patterns = [

        # Example:
        # Revenue for Q2 FY2027 was US$7,642 million.

        re.compile(
            rf"(?:consolidated\s+)?(?:total\s+)?"
            rf"revenue(?:\s+from\s+operations)?"
            rf"\s+(?:for|in)\s+{period_pattern}"
            rf"\s+(?:was|is)\s+"
            rf"{currency_pattern}\s*"
            rf"{amount_pattern}\s*{unit_pattern}",
            re.IGNORECASE
        ),

        # Example:
        # NVIDIA reported revenue of $96.221 billion in Q2 FY2027.

        re.compile(
            rf"(?:reported\s+)?(?:total\s+)?"
            rf"revenue(?:\s+from\s+operations)?"
            rf"\s+of\s+{currency_pattern}\s*"
            rf"{amount_pattern}\s*{unit_pattern}"
            rf"\s+in\s+{period_pattern}",
            re.IGNORECASE
        )
    ]

    records = []

    for pattern in patterns:

        for match in pattern.finditer(text):

            groups = match.groups()

            if pattern == patterns[0]:
                period, currency, amount, unit = groups
            else:
                currency, amount, unit, period = groups

            currency = currency or ""

            if currency in ("₹", "â‚¹", "INR"):
                currency_name = "INR"
            elif currency in ("$", "US$", "USD"):
                currency_name = "USD"
            else:
                currency_name = ""

            records.append({
                "period": period.upper(),
                "amount": float(amount.replace(",", "")),
                "unit": (
                    f"{currency_name} {unit}"
                    if currency_name
                    else unit
                )
            })

    return records


def period_sort_key(period):

    period = period.upper()

    if period.startswith("Q"):

        quarter = int(period[1])

        year = int(
            re.search(r"FY(\d{4})", period).group(1)
        )

        return year, quarter

    match = re.search(r"FY(\d{4})-(\d{2})", period)

    if match:
        return int(match.group(1)), 5

    return 0, 0


def analyze_companies(documents):

    grouped_documents = defaultdict(
        lambda: {"texts": [], "source": None}
    )

    for doc in documents:

        text, metadata = get_document_data(doc)

        company = metadata.get("company", "Unknown Company")

        source = (
            metadata.get("source_url")
            or metadata.get("source")
            or "Not available"
        )

        key = company

        grouped_documents[key]["texts"].append(text)

        if grouped_documents[key]["source"] is None:
            grouped_documents[key]["source"] = source

    results = []

    for company, data in grouped_documents.items():

        combined_text = "\n".join(data["texts"])

        records = extract_revenue_records(combined_text)

        if not records:
            continue

        unique_records = {}

        for record in records:
            unique_records[record["period"]] = record

        records = sorted(
            unique_records.values(),
            key=lambda x: period_sort_key(x["period"])
        )

        current = records[-1]

        result = {
            "company": company,
            "period": current["period"],
            "current_revenue": current["amount"],
            "previous_period": None,
            "previous_revenue": None,
            "unit": current["unit"],
            "source": data["source"],
            "growth_percentage": None
        }

        if len(records) >= 2:

            previous = records[-2]

            if previous["unit"] == current["unit"]:

                result["previous_period"] = previous["period"]

                result["previous_revenue"] = previous["amount"]

                if previous["amount"] != 0:

                    growth = (
                        (current["amount"] - previous["amount"])
                        / previous["amount"]
                    ) * 100

                    result["growth_percentage"] = round(growth, 2)

        results.append(result)

    return results