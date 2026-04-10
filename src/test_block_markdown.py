import unittest
from block_markdown import (
    markdown_to_blocks, 
    block_to_block_type, 
    BlockType, 
    markdown_to_html_node,
    extract_title
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_block_types(self):
        # Heading
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        # Code
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        # Quote
        self.assertEqual(block_to_block_type("> quote\n> more quote"), BlockType.QUOTE)
        # Unordered list
        self.assertEqual(block_to_block_type("- list\n- item"), BlockType.ULIST)
        # Ordered list
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.OLIST)
        # Paragraph
        self.assertEqual(block_to_block_type("this is a paragraph"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Hello  "), "Hello")
        self.assertEqual(extract_title("\n\n# Title"), "Title")
        with self.assertRaises(Exception):
            extract_title("## This is an H2, not an H1")
        with self.assertRaises(Exception):
            extract_title("Just some text")

if __name__ == "__main__":
    unittest.main()