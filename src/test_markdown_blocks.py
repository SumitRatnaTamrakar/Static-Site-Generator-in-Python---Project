import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
    # Basic splitting into blocks
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

    # Extra blank lines (to ensure empty blocks are removed) – that’s what this second test checks
    def test_markdown_to_blocks_newlines(self):
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

    # A document with only one block (no blank lines)
    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block with **bold** text and `code`."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block with **bold** text and `code`."])

    # A document with leading or trailing newlines to ensure strip() works.
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """

This is a block with extra newlines around it

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a block with extra newlines around it"])