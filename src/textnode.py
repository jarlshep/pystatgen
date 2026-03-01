from enum import Enum

class TextType(Enum):

    PLAIN_TEXT = "plain_text"
    BOLD_TEXT = "bold_text"
    ITALIC_TEXT = "italic_text"
    CODE_TEXT = "code_text"
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