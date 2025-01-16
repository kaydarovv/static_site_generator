import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_basic(self):
        node1 = HTMLNode(tag="a", value="TEST CASE LINK")
        result = node1.props_to_html()
        print(result)
    
    def test_advanced(self):
        node1 = HTMLNode(tag="p", value="TEST CASE PARAGRAPH", props={"href": "https://www.google.com", "target": "_blank"})
        result = node1.props_to_html()
        print(result)
    
    def test_broken(self):
        node1 = HTMLNode(tag="h1", value="TEST CASE HEADING1", props={"href": "https://www.google.com", "target": "_blank"})
        result = node1.props_to_html()
        print(result)


if __name__ == "__main__":
    unittest.main()
