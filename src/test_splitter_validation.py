import unittest

from text_splitter import split_text

class TestTextSplitter(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(split_text(""), [])

    def test_short_text(self):
        text = "NVIDIA reported strong revenue growth."
        chunks = split_text(text)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_chunks_do_not_exceed_limit(self):
        text = "Financial data " * 300
        chunks = split_text(text, chunk_size=200, overlap=30)

        self.assertGreater(len(chunks), 1)

        for chunk in chunks:
            self.assertLessEqual(len(chunk), 200)

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            split_text("Financial data", chunk_size=0)

    def test_invalid_overlap(self):
        with self.assertRaises(ValueError):
            split_text("Financial data", chunk_size=100, overlap=100)

    def test_all_text_is_represented(self):
        text = "Revenue increased. Profit remained stable."
        chunks = split_text(text)

        combined_text = " ".join(chunks)

        self.assertIn("Revenue increased.", combined_text)
        self.assertIn("Profit remained stable.", combined_text)

    if __name__ == "__main__":
        unittest.main(verbosity=2)
