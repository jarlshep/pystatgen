from text_to_html import text_node_to_html_node
from textnode import TextNode
from htmlnode import HTMLNode

def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

def test_bold(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold node")

def test_code(self):
    node = TextNode("This is code", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is code")

def test_italic(self):
    node = TextNode("This is italic text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is italic text")

def test_link(self):
    node = TextNode("This is a link", TextType.LINK, dict({"href": "https://www.google.com"}))
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link")
    self.assertEqual(html_node.props, 'href="https://www.google.com"')

def test_image(self):
    node = TextNode("This is alt text for an image", TextType.IMAGE, dict({"src": "public/src/hello.jpg"}))
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "This is alt text for an image")
    self.assertEqual(html_node.props, 'src="public/src/hello.jpg"')
