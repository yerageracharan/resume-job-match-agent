import unittest
from io import BytesIO

from docx import Document

from documents import extract_text_from_bytes


class DocumentTests(unittest.TestCase):
    def test_reads_txt(self):
        self.assertEqual(extract_text_from_bytes(b"Python developer", "resume.txt"), "Python developer")

    def test_reads_docx_paragraphs_and_tables(self):
        doc = Document()
        doc.add_paragraph("Software Engineer")
        table = doc.add_table(rows=1, cols=2)
        table.cell(0, 0).text = "Python"
        table.cell(0, 1).text = "FastAPI"
        buffer = BytesIO()
        doc.save(buffer)
        content = extract_text_from_bytes(buffer.getvalue(), "resume.docx")
        self.assertIn("Software Engineer", content)
        self.assertIn("Python | FastAPI", content)

    def test_rejects_unknown_format(self):
        with self.assertRaises(ValueError):
            extract_text_from_bytes(b"ignored", "resume.exe")

    def test_rejects_empty_file(self):
        with self.assertRaises(ValueError):
            extract_text_from_bytes(b"", "resume.txt")


if __name__ == "__main__":
    unittest.main()
