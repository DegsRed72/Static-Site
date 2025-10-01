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
    
    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("span", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span href="https://www.google.com">child</span></div>')

    def test_to_html_with_parents_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), '<div href="https://www.google.com"><span>child</span></div>')
    
    def test_to_html_with_parents_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_parents_without_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child")
        child_node3 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span><span>child</span></div>")

    def test_to_html_with_nested_parent_nodes(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [parent_node])
        self.assertEqual(parent_node2.to_html(), "<div><div><span>child</span></div></div>")
if __name__ == "__main__":
    unittest.main()