from enum import Enum
from inline_markdown import *
from htmlnode import *
from textnode import *

class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def convert_ulist(block):
    full_text = ""
    lines = block.split("\n")
    for line in lines:
        just_text = line.lstrip("- ")
        text_nodes = text_to_textnodes(just_text)
        leaf_node_list = text_to_children(just_text)
        list_text = ParentNode("li", leaf_node_list).to_html()
        full_text += list_text
    return LeafNode("ul", full_text)

def convert_olist(block):
    full_text = ""
    lines = block.split("\n")
    for line in lines:
        just_text = line.lstrip(".0123456789 ")
        text_nodes = text_to_textnodes(just_text)
        leaf_node_list = text_to_children(just_text)
        list_text = ParentNode("li", leaf_node_list).to_html()
        full_text += list_text
    return LeafNode("ol", full_text)


def convert_code(block):
    just_text = block.removeprefix("```\n").removesuffix("```")
    just_text_2 = LeafNode("code", just_text).to_html()
    return LeafNode("pre", just_text_2)

def convert_quote(block):
    full_text = ""
    lines = block.split("\n")
    for line in lines:
        just_text = line.lstrip("> ")
        text_nodes = text_to_textnodes(just_text)
        if text_nodes == [TextNode(just_text, TextType.TEXT)]:
            full_text += just_text + "\n"
        else:
            leaf_node_list = []
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                leaf_node_list.append(html_node)
            bare_text = ParentNode("x", leaf_node_list).to_html() 
            # "x" tag is meaningless and part of the reworked definition of ParentNode.to_html() to return parsed bare text string for insertion as text without element tags
            # bare_text = new_p.replace("<x>", "").replace("</x>", "") - not needed anymore, above comment
            full_text += bare_text + "\n"
    return LeafNode("blockquote", full_text)

def convert_heading(block):

    if block.startswith("# "):
        heading_size = "h1"
    if block.startswith("## "):
        heading_size = "h2"
    if block.startswith("### "):
        heading_size = "h3"
    if block.startswith("#### "):
        heading_size = "h4"
    if block.startswith("##### "):
        heading_size = "h5"
    if block.startswith("###### "):
        heading_size = "h6"

    clean_text = block.lstrip("# ")
    leaf_node_list = text_to_children(clean_text)
    bare_text = ParentNode("x", leaf_node_list).to_html()
    # bare_text = new_p.replace("<x>", "").replace("</x>", ""), see comment within convert_quote

    return LeafNode(heading_size, bare_text)

def convert_p(text):
    clean_text = text.replace("\n", " ")
    leaf_node_list = text_to_children(clean_text)
    new_p = ParentNode("p", leaf_node_list)
    return LeafNode(None, new_p.to_html())

def text_to_children(text):
    node_list = []
    text_node_list = text_to_textnodes(text)
    for node in text_node_list:
        new_node = text_node_to_html_node(node)
        node_list.append(new_node)
    return node_list

def markdown_to_html_node(markdown):
    child_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARA:
            new_leaf_node = convert_p(block)

        if block_type == BlockType.HEADING:
            new_leaf_node = convert_heading(block)
            
        if block_type == BlockType.CODE:
            new_leaf_node = convert_code(block)

        if block_type == BlockType.QUOTE:
            new_leaf_node = convert_quote(block)

        if block_type == BlockType.ULIST:
            new_leaf_node = convert_ulist(block)

        if block_type == BlockType.OLIST:
            new_leaf_node = convert_olist(block)

        child_nodes.append(new_leaf_node)
    
    return ParentNode("div", child_nodes)



def block_to_block_type(markdown):
    
    lines = markdown.split("\n")

    if markdown.startswith(("###### ", "##### ", "#### ", "### ", "## ", "# ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARA
        return BlockType.QUOTE
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARA
        return BlockType.ULIST
    if markdown.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARA
            i += 1
        return BlockType.OLIST
    return BlockType.PARA 

    """ my less robust first attempt
    head = markdown.split(maxsplit=1)

    if markdown[0:3] == "```":
        block_type = "code"
    elif "#" in head:
        block_type = "heading"
    elif ">" in head:
        block_type = "quote"
    elif "-" in head:
        block_type = "unordered_list"
    elif "1." in head:
        block_type = "ordered_list"
    else:
        block_type = "paragraph"

    return BlockType(block_type)
    """

def markdown_to_blocks(markdown):
    blocks = []
    split_list = markdown.split("\n\n")
    for string in split_list:
        if string == "":
            continue
        string = string.strip()
        string = string.strip("\n")
        blocks.append(string)
    return blocks

