import unittest

from block_markdown import *
from htmlnode import *
from textnode import * 
from inline_markdown import *

class TestMarkdown(unittest.TestCase):
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

    def test_markdown_to_blocks_2(self):
        md = """
**This is bolded paragraph**


This is another paragraph with _italic_ text and `code` here

This is a new line
`code`
`code`

- This is a list
- with items
- and more
- items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "**This is bolded paragraph**",
                "This is another paragraph with _italic_ text and `code` here", 
                "This is a new line\n`code`\n`code`",
                "- This is a list\n- with items\n- and more\n- items",
            ],
        )

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

    def test_block_to_block_type_para(self):
        block = "This is a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.PARA,
            BlockType("paragraph")
        )

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.CODE,
            BlockType("code")
        )

    def test_block_to_block_type_heading1(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.HEADING,
            BlockType("heading")
        )

    def test_block_to_block_type_heading4(self):
        block = "#### This is a size 4 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.HEADING,
            BlockType("heading")
        )

    def test_block_to_block_type_quote(self):
        block = ">This is a quote block\n> with 2 lines"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.QUOTE,
            BlockType("quote")
        )

    def test_block_to_block_type_ulist(self):
        block = "- This is an unordered list\n- with 2 lines"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.ULIST,
            BlockType("unordered_list")
        )

    def test_block_to_block_type_olist(self):
        block = "1. This is an ordered list\n2. with 2 entries"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type.OLIST,
            BlockType("ordered_list")
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # my tests of markdown_to_html_node
    def test_only_paras(self):
        md = """
This _is_ a paragraph
with 2 lines separated by a new line character

This **is** also a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This <i>is</i> a paragraph with 2 lines separated by a new line character</p><p>This <b>is</b> also a paragraph</p></div>",
        )

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

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
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

    def test_blockquote(self):
        md = """
> This is a block quote
> 
> with a second paragraph
> 
> and _some_ **inline** stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote\n\nwith a second paragraph\n\nand <i>some</i> <b>inline</b> stuff\n</blockquote></div>",
        )

    def test_ulist(self):
        md = """
- This is a list
- with a **few** items
- and some _inline_ stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with a <b>few</b> items</li><li>and some <i>inline</i> stuff</li></ul></div>",
        )

    def test_olist(self):
        md = """
1. This is an ordered list
2. with a **few** items
3. and some _inline_ stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with a <b>few</b> items</li><li>and some <i>inline</i> stuff</li></ol></div>",
        )

    # boot.dev tests of markdown_to_html_node
    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()