import unittest

from textnode import TextNode, TextType
from inline_md import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Test 1: Basic splitting with code
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT
        
        # Test 2: Node with no delimiters
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes[0].text == "Plain text without delimiters"
        assert new_nodes[0].text_type == TextType.TEXT

        # Test 3: Node that isn't TEXT type
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert new_nodes[0].text == "Already bold"
        assert new_nodes[0].text_type == TextType.BOLD

        # Test 4: Unmatched delimiters
        with self.assertRaises(Exception):
            node = TextNode("Unmatched `delimiter", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)

        # Test 5: Multiple delimiters
        node = TextNode("This is text with a *italic block* word and with *another italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert len(new_nodes) == 5
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "italic block"
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text == " word and with "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "another italic block"
        assert new_nodes[3].text_type == TextType.ITALIC
        assert new_nodes[4].text == " word"
        assert new_nodes[4].text_type == TextType.TEXT

        # Test 5: Empty delimiters
        node = TextNode("This is text with empty ** delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with empty "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == ""
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text == " delimiters"
        assert new_nodes[2].text_type == TextType.TEXT
        

if __name__ == "__main__":
    unittest.main()