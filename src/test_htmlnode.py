from platform import node
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

# --------------------------------------------------------------------------
# Tests for HTMLNode class
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# Tests for ParentNode class
# --------------------------------------------------------------------------

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

def test_to_html_with_children_2(self):
    node = ParentNode(
    "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    self.assertEqual(
        node.to_html(),
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    )

def test_to_html_with_no_tag_raises_value_error(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode(None, [child_node])
    with self.assertRaises(ValueError):
        parent_node.to_html()\
        
def test_to_html_with_no_tag_raises_value_error_2(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("", [child_node])
    with self.assertRaises(ValueError):
        parent_node.to_html()

def test_to_html_with_no_children_raises_value_error(self):
    parent_node = ParentNode("div", [])
    with self.assertRaises(ValueError):
        parent_node.to_html()

def test_to_html_with_no_children_raises_value_error_2(self):
    parent_node = ParentNode("div", None)
    with self.assertRaises(ValueError):
        parent_node.to_html()

def test_to_html_with_attributes(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
    self.assertEqual(
        parent_node.to_html(),
        '<div class="container" id="main"><span>child</span></div>'
    )

def test_to_html_with_multiple_children(self):
    child_1 = LeafNode("h1", "Title")
    child_2 = LeafNode("p", "This is a paragraph.")
    parent_node = ParentNode("div", [child_1, child_2])
    self.assertEqual(
        parent_node.to_html(),
        "<div><h1>Title</h1><p>This is a paragraph.</p></div>"
    )

def test_html_with_great_grandchildren(self):
    great_grandchild = LeafNode("i", "great-grandchild")
    grandchild = ParentNode("b", [great_grandchild])
    child = ParentNode("span", [grandchild])
    parent = ParentNode("div", [child])
    self.assertEqual(
        parent.to_html(),
        "<div><span><b><i>great-grandchild</i></b></span></div>"
    )