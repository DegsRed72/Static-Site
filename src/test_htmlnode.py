import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node =  HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
            })
        message = node.props_to_html()
        self.assertEqual(message, ' href="https://www.google.com" target="_blank"')

    def test_different_props(self):
        node =  HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
            })
        message = node.props_to_html()
        node2 =  HTMLNode(None, None, None, {
            "href": "https://www.edge.com",
            "target": "_blank",
            })
        message2 = node2.props_to_html()
        self.assertNotEqual(message, message2)
    
    def test_no_props(self):
        node =  HTMLNode(None, None, None, None)
        message = node.props_to_html()
        self.assertEqual(message, "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Hello, world!</p>')

    def test_leaf_to_html_p_without_value(self):
        node = LeafNode("p", "")
        self.assertRaises(ValueError, node.to_html)

    def test_leat_to_html_p_without_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), node.value)
if __name__ == "__main__":
    unittest.main()