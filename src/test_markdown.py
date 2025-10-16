import unittest

from textnode import *
from markdown import *

class Test_Markdown(unittest.TestCase):

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_incorrect_delimiter(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "_", TextType.BOLD)

    def test_odd_number_delimiters(self):
        node = TextNode("This is text with a **bold block word", TextType.PLAIN)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_nonplain_text_type(self):
        node = TextNode("This is text with a **bold block** word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a **bold block** word", TextType.BOLD)])

    def test_multiple_nodes(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        node2 = TextNode("This is text with another **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is text with another ", TextType.PLAIN),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ])
    
    def test_multiple_nodes_with_different_types(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        node2 = TextNode("This is bolded text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is bolded text", TextType.BOLD),
        ])
    
    def test_node_with_no_delimiters(self):
        node = TextNode("This is text with no bold block word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with no bold block word", TextType.PLAIN)])

    def test_node_not_being_TextNode(self):
        node = "hello"
        self.assertRaises(Exception, split_nodes_delimiter, node, "**", TextType.BOLD)

    def test_node_with_edge_delimiters(self):
        node = TextNode("**Bolded_word**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.PLAIN),
            TextNode("Bolded_word", TextType.BOLD),
            TextNode("", TextType.PLAIN),
            ])
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_no_markdown_images(self):
        matches = extract_markdown_images("This is text with no image")
        self.assertListEqual([], matches)

    def test_no_image_alt_text_or_url(self):
        self.assertEqual(extract_markdown_images("![]()"), [("", "")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_no_markdown_links(self):
        matches = extract_markdown_links("This is text with no link")
        self.assertListEqual([], matches)

    def test_no_link_anchor_or_url(self):
        self.assertEqual(extract_markdown_links("[]()"), [("", "")])


    def test_links_do_not_match_images(self):
        text = "![img](http://x.png) and [link](http://x.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "http://x.com")])

    def test_disallow_interior_brackets_and_parenthesis(self):
        self.assertEqual(extract_markdown_images("![a[b]](u)"), [])
        self.assertEqual(extract_markdown_images("![a](u(v))"), [])
        self.assertEqual(extract_markdown_links("[a[b]](u)"), [])
        self.assertEqual(extract_markdown_links("[a](u(v))"), [])

if __name__ == "__main__":
    unittest.main()