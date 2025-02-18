import unittest
from generate_page import extract_title

class TestExtractHeader(unittest.TestCase):
    def test_basic_case(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_multiple_spaces(self):
        self.assertEqual(extract_title("#    Hello"), "Hello")
    
    def test_text_before_after(self):
        text = """
        Some text here
        # My Title
        More text here
        """
        self.assertEqual(extract_title(text), "My Title")
    
    def test_extra_whitespace(self):
        self.assertEqual(extract_title("#    My Title    "), "My Title")
    
    def test_multiple_headers(self):
        text = """
        # First Title
        ## Second Title
        # Another Title
        """
        self.assertEqual(extract_title(text), "First Title")
    
    def test_no_header(self):
        text = """
        No header here
        Just some text
        ## h2 header
        """
        with self.assertRaises(Exception) as context:
            extract_title(text)
        self.assertEqual(str(context.exception), "No header h1(# ) was found")

if __name__ == '__main__':
    unittest.main()