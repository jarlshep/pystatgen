import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    
    def test_eq(self):
        test_dict = dict({"href" : "https://google.com", "style" : "bold"})
        node = HTMLNode("a", "https://google.com", None, test_dict)
        node2 = HTMLNode("a", "https://google.com", None, test_dict)
        self.assertEqual(repr(node), repr(node2))

    def test_not_eq(self):
        test_dict = {"href" : "https://google.com", "style" : "bold"}
        node = HTMLNode("a", "https://google.com", None, test_dict)
        node2 = HTMLNode("p", "Google is awesome!")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("p", "Google is awesome!")
        self.assertEqual("HTMLNode(p, Google is awesome!, None, None)", repr(node))

    def test_props_to_html(self):
        test_dict = dict({"href" : "https://google.com", "style" : "bold"})
        node = HTMLNode("a", "https://google.com", None, test_dict)
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://google.com" style="bold"')

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
        

if __name__ == "__main__":
    unittest.main()