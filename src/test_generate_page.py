import unittest

from generate_page import *

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = "# Title"
        title = extract_title(md)
        self.assertEqual(title, "Title")
    
    def test_extract_title_wrong_heading(self):
        md = "## Heading"
        self.assertRaises(Exception, extract_title, md)

    def test_extract_title_no_heading(self):
        md = "Heading"
        self.assertRaises(Exception, extract_title, md)

if __name__ == "__main__":
    unittest.main()