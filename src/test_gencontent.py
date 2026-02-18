import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    
    def test_simple_heading(self):
        heading = "# Heading"
        extracted_title = extract_title(heading)
        self.assertEqual(extracted_title, "Heading")

    def test_messsy_whitespaces(self):
        heading = " # Title With Spaces "
        with self.assertRaises(Exception):
            extracted_title = extract_title(heading)

    def test_other_headers(self):
        heading = "## Subheading"
        with self.assertRaises(Exception):
            extracted_title = extract_title(heading)
    
    def test_no_header_at_all(self):
        heading = "This is just plain text"
        with self.assertRaises(Exception):
            extracted_title = extract_title(heading)

    def test_the_middle_h1(self):
        heading = """
Welcome to my site.
# The Real Title
Hope you enjoy!
"""
        extracted_title = extract_title(heading)
        self.assertEqual(extracted_title, "The Real Title")
        