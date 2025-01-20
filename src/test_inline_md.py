import unittest
from inline_md import extract_markdown_images, extract_markdown_links

class TestMarkdownImageExtraction(unittest.TestCase):
    def test_single_image(self):
        text = "![alt text](https://example.com/image.jpg)"
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_multiple_images(self):
        text = """
        ![first image](http://first.com/1.png)
        Some text here
        ![second image](http://second.com/2.jpg)
        """
        expected = [
            ("first image", "http://first.com/1.png"),
            ("second image", "http://second.com/2.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])
    
    def test_no_images(self):
        text = "Just some regular text with [link](http://example.com)"
        self.assertEqual(extract_markdown_images(text), [])
    
    def test_special_characters(self):
        text = """![image with spaces!](http://example.com/image with spaces.jpg)
        ![image-with-dashes](http://example.com/image-2.png)
        ![image_with_underscores](http://example.com/image_3.jpg)"""
        expected = [
            ("image with spaces!", "http://example.com/image with spaces.jpg"),
            ("image-with-dashes", "http://example.com/image-2.png"),
            ("image_with_underscores", "http://example.com/image_3.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_single_link(self):
        text = "[Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = """
        [First Link](http://first.com)
        Some text here
        [Second Link](http://second.com)
        """
        expected = [
            ("First Link", "http://first.com"),
            ("Second Link", "http://second.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_no_links(self):
        text = "Just some regular text with ![image](http://example.com/img.jpg)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_special_characters(self):
        text = """[Link with spaces](http://example.com/page with spaces)
        [link-with-dashes](http://example.com/page-2)
        [link_with_underscores](http://example.com/page_3)"""
        expected = [
            ("Link with spaces", "http://example.com/page with spaces"),
            ("link-with-dashes", "http://example.com/page-2"),
            ("link_with_underscores", "http://example.com/page_3")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == '__main__':
    unittest.main()