from textnode import TextNode
from htmlnode import HTMLNode

#self.text = text
#self.text_type = TextType(txt_typ) , self.text_type.value
#self.url = url

def text_node_to_html_node(text_node):
    match text_node.text_type.value:
        case "TEXT": # This should return a LeafNode with no tag, just a raw text value.
            return LeafNode(None, text_node.text, None)
        case "BOLD": # This should return a LeafNode with a "b" tag and the text
            return LeafNode("b", text_node.text, None)
        case "ITALIC": # "i" tag, text
            return LeafNode("i", text_node.text, None)
        case "CODE": # "code" tag, text
            return LeafNode("code", text_node.text, None)
        case "LINK": # "a" tag, anchor text, and "href" prop
            return LeafNode("a", text_node.text, dict({"href": text_node.url}))
        case "IMAGE": # "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
            return LeafNode("img", "", dict({"src": text_node.url, "alt": text_node.text}))

