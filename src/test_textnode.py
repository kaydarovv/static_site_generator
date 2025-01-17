import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_ineq_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_ineq_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node1, node2)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_to_leaf_node(self):
        # Test conversion of regular text node
        text_node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just plain text")
        self.assertIsNone(html_node.props)
        
    def test_link_to_leaf_node(self):
        # Test conversion of link node with URL
        text_node = TextNode(
            "Click me",
            TextType.LINK,
            "https://www.example.com"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.example.com"}
        )
        
    def test_image_to_leaf_node(self):
        # Test conversion of image node
        text_node = TextNode(
            "Cool image",
            TextType.IMAGE,
            "https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.jpg",
                "alt": "Cool image"
            }
        )

if __name__ == "__main__":
    unittest.main()
