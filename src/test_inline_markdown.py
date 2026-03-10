import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_node_b_end(self):
        node = TextNode("This is text with **bold at the end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(new_nodes, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold at the end", TextType.BOLD),
        ])

    def test_node_i_beginning(self):
        node = TextNode("_Italic_ text at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(new_nodes, [
            TextNode("Italic", TextType.ITALIC),
            TextNode(" text at the beginning", TextType.TEXT),
        ])

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    # image and link extraction
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link to google](https://www.google.com)"
        )
        self.assertListEqual([("link to google", "https://www.google.com")], matches)

    def test_extract_markdown_image_2(self):
        matches = extract_markdown_images(
            "![symbol](images/123/345/zjjcJKZ.png)"
        )
        self.assertListEqual([("symbol", "images/123/345/zjjcJKZ.png")], matches)

    def test_extract_markdown_link_2(self):
        matches = extract_markdown_links(
            "[Click here](https://www.example.com)"
        )
        self.assertListEqual([("Click here", "https://www.example.com")], matches)

    # split text into nodes at images and links 
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and little more text after.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and little more text after.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with a [link to google](https://www.google.com) and a [link to boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a [link to google](https://www.google.com) and a [link to boot.dev](https://boot.dev)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link to google](https://www.google.com) and a [link to boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link to boot.dev", TextType.LINK, "https://boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_link_2(self):
        node = TextNode(
            "This is text with a [link to google](https://www.google.com) and a [link to boot.dev](https://boot.dev) and a litte more text after.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link to boot.dev", TextType.LINK, "https://boot.dev"
                ),
                TextNode(" and a litte more text after.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode(
            "This is text with no links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with no links.",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "[sample link](https://www.example.COM)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("sample link", TextType.LINK, "https://www.example.COM"),
            ],
            new_nodes,
        )

    # test all splitting functions together
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list
        )
    
    def test_text_to_textnodes_wayward_delimiter(self):
        with self.assertRaises(Exception):
            text = "This is **text** with an _italic_ word and _a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            text_to_textnodes(text)
   
    def test_text_to_textnodes(self):
        text = "**text**_italic_`code block`![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        node_list = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list
        )

if __name__ == "__main__":
    unittest.main()