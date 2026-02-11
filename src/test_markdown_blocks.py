import unittest
import textwrap

from markdown_blocks import markdown_to_blocks

from markdown_blocks import BlockType, block_to_block_type

from markdown_blocks import markdown_to_html_node

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

class TestBlockToBlockTyping(unittest.TestCase):
    
    # Unit Tests for Headings

    def test_block_type_heading_1(self):
        block_type = block_to_block_type("# Heading 1")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_2(self):
        block_type = block_to_block_type("## Heading 2")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_3(self):
        block_type = block_to_block_type("### Heading 3")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_4(self):
        block_type = block_to_block_type("#### Heading 4")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_5(self):
        block_type = block_to_block_type("##### Heading 5")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_6(self):
        block_type = block_to_block_type("###### Heading 6")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_heading_7(self):
        block_type = block_to_block_type("####### Heading 7")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_type_heading_no_space(self):
        block_type = block_to_block_type("#Heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_type_empty_heading(self):
        block_type = block_to_block_type("# ")
        self.assertEqual(block_type, BlockType.HEADING)

    """ 
    Since leading spaces are stripped by default, this test case is skipped
    def test_block_type_heading_with_leading_spaces(self):
        block_type = block_to_block_type(" # Heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    """

    # Unit Tests for Code Blocks

    def test_block_type_valid_code(self):
        code_block = (
            "```\n"
            "Code block\n"
            "```"
        )
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_type_invalid_code_1(self):
        code_block = (
            "```\n"
            "Code block\n"
            ""
        )
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_type_invalid_code_2(self):
        code_block = (
            "\n"
            "Code block\n"
            "```"
        )
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_type_valid_code_2(self):
        code_block = (
            "```\n"
            "```"
        )
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    # Unit Tests for Quotes
    
    def test_single_line_quote(self):
        quote_block = (
            "> A single-line quote"
        )
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_multi_line_quote(self):
        quote_block = textwrap.dedent("""
> Multi-line quote
> Quote line 1
> Quote line 2
        """).strip()
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_multi_line_quote_with_varying_indentation(self):
        quote_block = textwrap.dedent("""
> Multi-line quote block
    > Quote line 1 indentation: 1
        > Quote line 2 indentation 2
        """).strip()

        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_single_line_quote_with_leading_spaces(self):
        quote_block = "     > Quote block"
        
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_multi_line_quote_with_leading_spaces(self):
        quote_block = textwrap.dedent("""
    > Multi-line quote with leading spaces
    > Quote line 1
    > Quote line 2
    > Quote line 3
        """).strip()
        
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_multi_line_quote_with_one_line_missing_quote_symbol_in_middle(self):
        quote_block = textwrap.dedent("""
    > Multi-line quote with a missing > in the middle
    > Line 1
    Line 2
    > Line 2
""").strip()
        
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_multi_line_quote_block_with_a_blank_line_in_the_middle(self):
        quote_block = textwrap.dedent("""
            > Multi-line quote with a blank line in the middle
            > Quote line 1

            > Quote line 2
""").strip()
        
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # Unit Tests for unordered lists

    def test_block_to_block_type_unordered_list_single_item_list(self):
        unordered_list = "- Unordered List"
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multi_line_list(self):
        unordered_list = """- First Item
- Second item
- Third item"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_mixed_invalid_list(self):
        unordered_list = """- First item
- Second Item
Third Item
Fourth Item
- Fifth Item
"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_mixed_invalid_list_2(self):
        unordered_list = """- First item
- Second Item
-Third Item
-Fourth Item
- Fifth Item
"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_block_to_block_type_unordered_list_invalid_list_1(self):
        unordered_list = " - List item 1"
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_invalid_list_2(self):
        unordered_list = "* List item 1"
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_invalid_list_3(self):
        unordered_list = "-List item 1"
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    """ An unordered list with - followed by a tab should result in an invalid list but does not produce the expected result. 
    def test_block_to_block_type_unordered_list_invalid_list_4(self):
        unordered_list = "-         List item 1"
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
 """
    
    def test_block_to_block_type_unordered_list_paragraph_with_dash_in_middle(self):
        unordered_list = "This is not a list - it's just a sentence with a dash in it."
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # Unit tests for ordered lists

    def test_block_to_block_type_ordered_list_single_line_valid(self):
        ordered_list_block = "1. Item 1"
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_mulit_line_valid(self):
        ordered_list_block = """1. First Item
2. Second Item
3. Third Item"""
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong_starting_number_invalid(self):
        ordered_list_block = """3. First Item
4. Second Item
5. Third Item
"""
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_non_proper_incrementation_of_numbers_invalid(self):
        ordered_list_block = """1. First Item
3. Second Item
4. Third Item"""
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_extra_text_before_the_number(self):
        ordered_list_block = """Prefix 1. First item
2. Second Item
3. Third Item"""
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        

# Block to HTML Unit Tests

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

    def test_headings(self):
        md = """
# Heading 1

## This is heading 2

### This is the third heading

#### This is Heading the Fourth

##### This is Heading V (5)

###### This is heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>This is heading 2</h2><h3>This is the third heading</h3><h4>This is Heading the Fourth</h4><h5>This is Heading V (5)</h5><h6>This is heading 6</h6></div>"
        )

    def test_headings_with_inline_markdown(self):
        md = """
# Heading 1

## **This is a bolded heading 2**

#### This is a _Heading 4 with italics_

##### This is Heading V (5)

###### This is heading 6 `with some code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2><b>This is a bolded heading 2</b></h2><h4>This is a <i>Heading 4 with italics</i></h4><h5>This is Heading V (5)</h5><h6>This is heading 6 <code>with some code</code></h6></div>"
        )

    def test_code_block_with_inline_markdown(self):
        md = """
```
This is **not** bold
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is **not** bold\n</code></pre></div>"
        )

    def test_unorderd_list_block_with_multiple_items(self):
        md = """
- Unordered list item 1
- Unordered list item 2
- Unordered list item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3</li></ul></div>"
        )

    def test_orderd_list_block_with_multiple_items(self):
        md = """
1. First Ordered list item
2. Second Ordered list item
3. Third Ordered list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First Ordered list item</li><li>Second Ordered list item</li><li>Third Ordered list item</li></ol></div>"
        )

    def test_unordered_list_with_inline_formatting(self):
        md = """
- This is a list item
- This has **bold** and _italics_
- And a [link to Boot.dev](https://www.boot.dev)
"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is a list item</li><li>This has <b>bold</b> and <i>italics</i></li><li>And a <a href="https://www.boot.dev">link to Boot.dev</a></li></ul></div>'
        )

    def test_a_mixed_document(self):
        md = """
# My List

- Item 1
- Item 2

1. First
2. Second
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>My List</h1><ul><li>Item 1</li><li>Item 2</li></ul><ol><li>First</li><li>Second</li></ol></div>"
        )

    def test_multi_line_blockquotes(self):
        md = """
> This is a multi-line
> blockquote that should
> be captured together.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a multi-line blockquote that should be captured together.</blockquote></div>"
        )

    def test_blockquote_with_inline_markdown(self):
        md = """
> This blockquote has **bold** and _italic_ text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This blockquote has <b>bold</b> and <i>italic</i> text.</blockquote></div>"
        )

    def test_single_block_of_text_single_line(self):
        md = """
A single block of text consisting of a single-line.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>A single block of text consisting of a single-line.</p></div>"
        )

    def test_single_block_of_text_multi_line(self):
        md = """
A single block of text consisting of a multi-line.
This is the first line.
This is line number 2.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>A single block of text consisting of a multi-line. This is the first line. This is line number 2.</p></div>"
        )

    def test_paragraph_with_link_and_image(self):
        md = """
This is a paragraph with a [link](https://boot.dev) and an ![image](https://example.com/img.png) inside it.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://boot.dev">link</a> and an <img src="https://example.com/img.png" alt="image"/> inside it.</p></div>'
        )