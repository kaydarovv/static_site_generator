import unittest

from textnode import TextNode, TextType
from inline_md import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes


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

    def test_split_nodes_link(self):
        # Test 1: Single link
        node = TextNode("Start [link](url) end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Start "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "link"
        assert new_nodes[1].text_type == TextType.LINK
        assert new_nodes[2].text == " end"
        assert new_nodes[2].text_type == TextType.TEXT

        # Test 2: Two links
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])

        assert len(new_nodes) == 4
        assert new_nodes[0].text == "This is text with a link "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "to boot dev"
        assert new_nodes[1].text_type == TextType.LINK
        assert new_nodes[1].url == "https://www.boot.dev"
        assert new_nodes[2].text == " and "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "to youtube"
        assert new_nodes[3].text_type == TextType.LINK
        assert new_nodes[3].url == "https://www.youtube.com/@bootdotdev"

        # Test 3: Empty input
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert new_nodes[0].text == ""
        assert new_nodes[0].text_type == TextType.TEXT

        # Test 4: No links
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert new_nodes[0].text == "Just plain text"
        assert new_nodes[0].text_type == TextType.TEXT

        # Test 5: Adjacent links
        node = TextNode("Start [one](url1)[two](url2) end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "Start "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "one"
        assert new_nodes[1].text_type == TextType.LINK
        assert new_nodes[2].text == "two"
        assert new_nodes[2].text_type == TextType.LINK
        assert new_nodes[3].text == " end"
        assert new_nodes[3].text_type == TextType.TEXT
        

    def test_split_nodes_image(self):
        # Test 1: Single image
        node = TextNode("Start ![image](url) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Start "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "image"
        assert new_nodes[1].text_type == TextType.IMAGE
        assert new_nodes[2].text == " end"
        assert new_nodes[2].text_type == TextType.TEXT

        # Test 2: Two images
        node = TextNode("This is text with an image ![to boot dev](imgs/boot.jpg) and ![to youtube](imgs/www.youtube.com/@bootdotdev.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "This is text with an image "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "to boot dev"
        assert new_nodes[1].text_type == TextType.IMAGE
        assert new_nodes[1].url == "imgs/boot.jpg"
        assert new_nodes[2].text == " and "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "to youtube"
        assert new_nodes[3].text_type == TextType.IMAGE
        assert new_nodes[3].url == "imgs/www.youtube.com/@bootdotdev.png"

        # Test 3: Empty input
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert new_nodes[0].text == ""
        assert new_nodes[0].text_type == TextType.TEXT

        # Test 4: No images
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert new_nodes[0].text == "Just plain text"
        assert new_nodes[0].text_type == TextType.TEXT

        # Test 5: Adjacent images
        node = TextNode("Start ![one](url1)![two](url2) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "Start "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "one"
        assert new_nodes[1].text_type == TextType.IMAGE
        assert new_nodes[2].text == "two"
        assert new_nodes[2].text_type == TextType.IMAGE
        assert new_nodes[3].text == " end"
        assert new_nodes[3].text_type == TextType.TEXT


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        assert len(new_nodes) == 10
        assert new_nodes[0].text == "This is "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "text"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " with an "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "italic"
        assert new_nodes[3].text_type == TextType.ITALIC
        assert new_nodes[4].text == " word and a "
        assert new_nodes[4].text_type == TextType.TEXT
        assert new_nodes[5].text == "code block"
        assert new_nodes[5].text_type == TextType.CODE
        assert new_nodes[6].text == " and an "
        assert new_nodes[6].text_type == TextType.TEXT
        assert new_nodes[7].text == "obi wan image"
        assert new_nodes[7].text_type == TextType.IMAGE
        assert new_nodes[7].url == "https://i.imgur.com/fJRm4Vk.jpeg"
        assert new_nodes[8].text == " and a "
        assert new_nodes[8].text_type == TextType.TEXT
        assert new_nodes[9].text == "link"
        assert new_nodes[9].text_type == TextType.LINK
        assert new_nodes[9].url == "https://boot.dev"

        # Test 1: Multiple of the same type
        text1 = "This is **bold** and this is also **bold**"
        nodes1 = text_to_textnodes(text1)
        assert len(nodes1) == 5
        assert nodes1[0].text == "This is "
        assert nodes1[0].text_type == TextType.TEXT
        assert nodes1[1].text == "bold"
        assert nodes1[1].text_type == TextType.BOLD
        assert nodes1[2].text == " and this is also "
        assert nodes1[2].text_type == TextType.TEXT
        assert nodes1[3].text == "bold"
        assert nodes1[3].text_type == TextType.BOLD
        assert nodes1[4].text == ""
        assert nodes1[4].text_type == TextType.TEXT

        # Test 3: Multiple different types
        text3 = "Here's `code` with *italic* and **bold** and ![image](test.jpg)"
        nodes3 = text_to_textnodes(text3)
        assert len(nodes3) == 8
        assert nodes3[0].text == "Here's "
        assert nodes3[0].text_type == TextType.TEXT
        assert nodes3[1].text == "code"
        assert nodes3[1].text_type == TextType.CODE
        assert nodes3[2].text == " with "
        assert nodes3[2].text_type == TextType.TEXT
        assert nodes3[3].text == "italic"
        assert nodes3[3].text_type == TextType.ITALIC
        assert nodes3[4].text == " and "
        assert nodes3[4].text_type == TextType.TEXT
        assert nodes3[5].text == "bold"
        assert nodes3[5].text_type == TextType.BOLD
        assert nodes3[6].text == " and "
        assert nodes3[6].text_type == TextType.TEXT
        assert nodes3[7].text == "image"
        assert nodes3[7].text_type == TextType.IMAGE
        assert nodes3[7].url == "test.jpg"

        # Test 4: Bad formatting
        text4 = "This is *italic but missing end"
        with self.assertRaises(Exception):
            text_to_textnodes(text4)

        # Test 5: Links and images together
        text5 = "![image](test.jpg) and [link](https://boot.dev)"
        nodes5 = text_to_textnodes(text5)
        assert len(nodes5) == 3
        assert nodes5[0].text == "image"
        assert nodes5[0].text_type == TextType.IMAGE
        assert nodes5[0].url == "test.jpg"
        assert nodes5[1].text == " and "
        assert nodes5[1].text_type == TextType.TEXT
        assert nodes5[2].text == "link"
        assert nodes5[2].text_type == TextType.LINK
        assert nodes5[2].url == "https://boot.dev"


if __name__ == "__main__":
    unittest.main()