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

    def test_split_nodes_with_no_image(self):
        node = TextNode("This is text with no image", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This is text with no image", TextType.PLAIN)])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_with_ending_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) pineapple",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" pineapple", TextType.PLAIN),
            ],
            new_nodes,
        )
    def test_one_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    def test_more_than_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a third ![third image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a third ", TextType.PLAIN),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com) and another [second link](https://i.imgur.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        text_to_textnode(text))

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

    def test_empty_block(self):
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
    
    def test_single_block(self):
        md = """
This is **bolded** paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
    def test_no_blocks(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )
if __name__ == "__main__":
    unittest.main()