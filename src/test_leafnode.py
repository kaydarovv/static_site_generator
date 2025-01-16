import unittest

from htmlnode import HTMLNode, LeafNode



class TestLeafNode(unittest.TestCase):
    def test_basic(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        result = node1.to_html()
        print(result)
    
    def test_full(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = node1.to_html()
        print(result)

    def test_full(self):
        node1 = LeafNode(tag="h1", value="TEST CASE HEADING1", props={"href": "https://www.google.com", "target": "_blank"})
        result = node1.to_html()
        print(result)
    

if __name__ == "__main__":
    unittest.main()