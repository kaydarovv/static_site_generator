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


    def test_block_to_block_type(self):
        #oneline code
        block = "```This is a code text```"
        block_type = block_to_block_type(block)
        assert block_type == "code"

        #multiline code
        block = "```This is a code text \n that is multiline \n and function hopefully detects that its still a code```"
        block_type = block_to_block_type(block)
        assert block_type == "code"

        #oneline paragraph
        block = "This is a paragraph text"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        #multiline paragraph
        block = "This is a paragraph text \n that is multiline \n and function hopefully detects that its still a simple paragraph"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 1: H1 heading
        block = "# Heading level 1"
        block_type = block_to_block_type(block)
        assert block_type == "heading"

        # Test case 2: H6 heading (maximum level)
        block = "###### Heading level 6"
        block_type = block_to_block_type(block)
        assert block_type == "heading"

        # Test case 3: Invalid - too many hashtags
        block = "####### Exceeds maximum level"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 4: Invalid - no space after hashtags
        block = "#NoSpaceAfterHash"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 5: Invalid - multiple spaces after hashtags
        block = "##  Multiple spaces"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 6: Invalid - leading space before hashtags
        block = " # Leading space"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

         # Test case 1: Single line quote
        block = ">This is a quote"
        block_type = block_to_block_type(block)
        assert block_type == "quote"

        # Test case 2: Multiline quote
        block = ">First line of quote\n>Second line of quote\n>Third line"
        block_type = block_to_block_type(block)
        assert block_type == "quote"

        # Test case 3: Invalid - missing prefix on second line
        block = ">First line\nSecond line without prefix"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 4: Invalid - space before >
        block = " >Invalid quote format"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 5: Empty quote lines
        block = ">\n>\n>Last line"
        block_type = block_to_block_type(block)
        assert block_type == "quote"

        # Test case 1: Valid single item list
        block = "1. First item"
        block_type = block_to_block_type(block)
        assert block_type == "ordered_list"

        # Test case 2: Valid multi-item list
        block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_block_type(block)
        assert block_type == "ordered_list"

        # Test case 3: Invalid - wrong starting number
        block = "2. Starting with two"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 4: Invalid - missing space after dot
        block = "1.No space here"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 5: Invalid - incorrect format
        block = " 1. Leading space"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"

        # Test case 1: Valid single item unordered list with asterisk
        block = "* First item"
        block_type = block_to_block_type(block)
        assert block_type == "unordered_list"
        
        # Test case 2: Valid single item unordered list with hyphen
        block = "- First item"
        block_type = block_to_block_type(block)
        assert block_type == "unordered_list"
        
        # Test case 3: Valid multi-item list with asterisks
        block = "* First item\n* Second item\n* Third item"
        block_type = block_to_block_type(block)
        assert block_type == "unordered_list"
        
        # Test case 4: Valid multi-item list with hyphens
        block = "- First item\n- Second item\n- Third item"
        block_type = block_to_block_type(block)
        assert block_type == "unordered_list"
        
        # Test case 5: Valid mixed markers
        block = "* First item\n- Second item\n* Third item"
        block_type = block_to_block_type(block)
        assert block_type == "unordered_list"
        
        # Test case 6: Invalid - missing space after marker
        block = "*No space here"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"
        
        # Test case 7: Invalid - leading space
        block = " * Leading space"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"
        
        # Test case 8: Invalid - wrong marker
        block = "+ Invalid marker"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"
        
        # Test case 9: Invalid - inconsistent spacing
        block = "*  Extra space"
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"
        
        # Test case 10: Invalid - empty item
        block = "* "
        block_type = block_to_block_type(block)
        assert block_type == "paragraph"