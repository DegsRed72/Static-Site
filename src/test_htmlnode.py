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
        self.assertEqual(message, None)

if __name__ == "__main__":
    unittest.main()