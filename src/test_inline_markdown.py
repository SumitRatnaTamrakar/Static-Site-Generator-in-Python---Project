import unittest
from inline_markdown import (
    extract_markdown_links,
    extract_markdown_images,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_with_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with ![image1](https://i.imgur.com/image1.png) and ![image2](https://i.imgur.com/image2.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/image1.png"), ("image2", "https://i.imgur.com/image2.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev")
            ],
            matches,
        )

    def test_extract_markdown_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_images_with_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links."
        )
        self.assertListEqual([], matches)

    