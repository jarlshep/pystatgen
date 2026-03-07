from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"         # [anchor text](url)
    IMAGE = "image"       # ![alt text](url)


class TextNode():
    def __init__(self, text, txt_typ, url=None):
        self.text = text
        self.text_type = TextType(txt_typ)
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
   
    match text_node.text_type:
        case TextType.TEXT: # This should return a LeafNode with no tag, just a raw text value.
            return LeafNode(None, text_node.text)
        case TextType.BOLD: # This should return a LeafNode with a "b" tag and the text
            return LeafNode("b", text_node.text)
        case TextType.ITALIC: # "i" tag, text
            return LeafNode("i", text_node.text)
        case TextType.CODE: # "code" tag, text
            return LeafNode("code", text_node.text)
        case TextType.LINK: # "a" tag, anchor text, and "href" prop
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE: # "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid text type: {text_node.text_type}")

