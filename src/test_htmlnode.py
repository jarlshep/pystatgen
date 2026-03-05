import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    # LeafNode tests from boot.dev, mine were using my bad child class definition
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # ParentNode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("b", "Hello")
        child_node2 = LeafNode(None, " world")
        child_node3 = LeafNode("b", "!")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>Hello</b> world<b>!</b></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(Exception):
            ParentNode("div", None,).to_html()

    def test_to_html_with_no_tag(self):
        with self.assertRaises(Exception):
            child_node = LeafNode("p", "Yo!")
            ParentNode(None, [child_node],).to_html()

if __name__ == "__main__":
    unittest.main()