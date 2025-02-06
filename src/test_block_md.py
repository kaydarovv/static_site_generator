import unittest

from textnode import TextNode, TextType
from block_md import markdown_to_blocks, block_to_block_type


class TestBlocks(unittest.TestCase):
    # Test sample
    def test_split_nodes_delimiter(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        assert len(blocks) == 3
        assert blocks[0] == "# This is a heading"
        assert blocks[1] == "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        assert blocks[2] == "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        # Multiple lines
        text = """
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.

"""
        blocks = markdown_to_blocks(text)
        assert len(blocks) == 2
        assert blocks[0] == "# This is a heading"
        assert blocks[1] == "This is a paragraph of text. It has some **bold** and *italic* words inside of it."

        # One Block
        text = """
# This is a heading
"""
        blocks = markdown_to_blocks(text)
        assert len(blocks) == 1
        assert blocks[0] == "# This is a heading"


 