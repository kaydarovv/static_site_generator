import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_empty_markdown(self):
        with self.assertRaises(Exception):
            markdown_to_html_node("")
    
    def test_single_paragraph(self):
        md = "This is a simple paragraph"
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "p")
        self.assertEqual(len(html.children[0].children), 1)
        self.assertEqual(html.children[0].children[0].tag, None)
        self.assertEqual(html.children[0].children[0].value, "This is a simple paragraph")

    def test_heading_conversion(self):
        md = """# Heading 1

## Heading 2

### Heading 3"""
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 3)
        self.assertEqual(html.children[0].tag, "h1")
        self.assertEqual(html.children[1].tag, "h2")
        self.assertEqual(html.children[2].tag, "h3")
        self.assertEqual(html.children[0].children[0].value, "Heading 1")
        self.assertEqual(html.children[1].children[0].value, "Heading 2")
        self.assertEqual(html.children[2].children[0].value, "Heading 3")

    def test_unordered_list(self):
        md = """* First item
* Second item
* Third item"""
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "ul")
        self.assertEqual(len(html.children[0].children), 3)
        for child in html.children[0].children:
            self.assertEqual(child.tag, "li")
        self.assertEqual(html.children[0].children[0].children[0].value, "First item")
        self.assertEqual(html.children[0].children[1].children[0].value, "Second item")
        self.assertEqual(html.children[0].children[2].children[0].value, "Third item")

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "ol")
        self.assertEqual(len(html.children[0].children), 3)
        for child in html.children[0].children:
            self.assertEqual(child.tag, "li")
        self.assertEqual(html.children[0].children[0].children[0].value, "First item")
        self.assertEqual(html.children[0].children[1].children[0].value, "Second item")
        self.assertEqual(html.children[0].children[2].children[0].value, "Third item")

    def test_code_block(self):
        md = """```
def hello():
    print("world")
```"""
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "pre")
        self.assertEqual(len(html.children[0].children), 1)
        self.assertEqual(html.children[0].children[0].tag, "code")
        self.assertEqual(html.children[0].children[0].children[0].value, 'def hello():\n    print("world")')

    def test_blockquote(self):
        md = """> This is a quote
> Multiple lines"""
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "blockquote")
        self.assertEqual(html.children[0].children[0].value, "This is a quote\nMultiple lines")

    def test_mixed_inline_formatting(self):
        md = "This is **bold** and *italic* with `code`"
        html = markdown_to_html_node(md)
        self.assertEqual(len(html.children), 1)
        p_node = html.children[0]
        self.assertEqual(p_node.tag, "p")
        self.assertEqual(len(p_node.children), 7)
        self.assertEqual(p_node.children[0].value, "This is ")
        self.assertEqual(p_node.children[1].tag, "b")
        self.assertEqual(p_node.children[2].value, " and ")
        self.assertEqual(p_node.children[3].tag, "i")
        self.assertEqual(p_node.children[4].value, " with ")
        self.assertEqual(p_node.children[5].tag, "code")


if __name__ == "__main__":
    unittest.main()