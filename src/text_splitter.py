def split_text(text, chunk_size=700, overlap=100):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Prefer a paragraph or line boundary when one is nearby.
        if end < text_length:
            search_start = start + chunk_size // 2

            paragraph_boundary = text.rfind("\n\n", search_start, end)
            line_boundary = text.rfind("\n", search_start, end)
            space_boundary = text.rfind(" ", search_start, end)

            boundary = max(
                paragraph_boundary,
                line_boundary,
                space_boundary
            )

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Move backwards to retain overlap with the next chunk.
        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks