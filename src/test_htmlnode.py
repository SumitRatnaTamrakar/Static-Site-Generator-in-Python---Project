import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode("p", "This is a paragraph", children=None, props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "text"})
        
    # With no props at all - e.g. HTMLNode(tag="p")
    def test_props_to_html_1(self):
        node = HTMLNode("p", "This is a paragraph", children=None)
        self.assertEqual(node.props_to_html(), "")

    # With empty props - e.g. HTMLNode(tag="p", props={}).
    def test_props_to_html_2(self):
        node = HTMLNode("p", "This is a paragraph", children=None, props={})
        self.assertEqual(node.props_to_html(), "")

    # Test props_to_html with multiple props - 
    # e. g. HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"}).
    def test_props_to_html_3(self):
        node = HTMLNode("a", "This is a link", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("div", "This is a div", children=None, props={"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=This is a div, children=None, props={'class': 'container'})")

    def test_repr_no_props(self):
        node = HTMLNode("span", "This is a span", children=None)
        self.assertEqual(repr(node), "HTMLNode(tag=span, value=This is a span, children=None, props=None)")

    def test_repr_no_children(self):
        node = HTMLNode("p", "This is a paragraph", props={"id": "para1", "class": "text-1"})
        self.assertEqual(repr(node), "HTMLNode(tag=p, value=This is a paragraph, children=None, props={'id': 'para1', 'class': 'text-1'})")

# --------------------------------------------------------------------------
# Tests for LeafNode class
# --------------------------------------------------------------------------

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_basic_tag_and_value(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_to_html_with_tag_with_attributes(self):
        node = LeafNode("a", "This is a link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">This is a link</a>')
    
    def test_to_html_with_raw_text_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_to_html_with_no_value_raises_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("img", "image.png", props={"alt": "An image", "width": "100"})
        self.assertEqual(repr(node), "LeafNode(tag=img, value=image.png, props={'alt': 'An image', 'width': '100'})")

