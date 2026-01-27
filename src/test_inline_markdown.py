import unittest
from inline_markdown import (
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link
    )

from textnode import TextNode, TextType

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

    # --------------------------------------------------------------------------
    # Tests for split_nodes_image function
    # --------------------------------------------------------------------------

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

# ---------------------------------------------------------------------------


    def test_split_nodes_image_with_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_images_with_no_images(self):
        node = TextNode("This is text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_images_with_single_image(self):
        node = TextNode(
            "Here is an image: ![sample image](https://i.imgur.com/sample.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("sample image", TextType.IMAGE, "https://i.imgur.com/sample.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_images_with_multiple_images(self):
        node = TextNode(
            "First image ![img1](https://i.imgur.com/img1.png) second image ![img2](https://i.imgur.com/img2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First image ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://i.imgur.com/img1.png"),
                TextNode(" second image ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://i.imgur.com/img2.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_image_at_start(self):
        node = TextNode(
            "![start image](https://i.imgur.com/start.png) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://i.imgur.com/start.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_image_at_end(self):
        node = TextNode(
            "This is at the end ![end image](https://i.imgur.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is at the end ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://i.imgur.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_a_mix_of_text_and_non_text_nodes(self):
        nodes = [
            TextNode("This is text with an ![image1](https://i.imgur.com/image1.png)", TextType.TEXT),
            TextNode("This is bold text", TextType.BOLD),
            TextNode("Another image here ![image2](https://i.imgur.com/image2.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/image1.png"),
                TextNode("This is bold text", TextType.BOLD),
                TextNode("Another image here ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/image2.png"),
            ],
            new_nodes,
        )

    # --------------------------------------------------------------------------
    # Tests for split_nodes_image function
    # --------------------------------------------------------------------------

    def test_split_node_links_with_no_links(self):
        node = TextNode("This is text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_node_links_with_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_single_link_only_content(self):
        node = TextNode(
            "[Only link](https://www.onlylink.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Only link", TextType.LINK, "https://www.onlylink.com"),
            ],
            new_nodes,
        )   

    def test_split_node_links_with_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_node_links_with_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_node_links_with_link_at_start(self):
        node = TextNode(
            "[Start link](https://www.start.com) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start link", TextType.LINK, "https://www.start.com"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_node_links_with_link_at_end(self):
        node = TextNode(
            "This is at the end [End link](https://www.end.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is at the end ", TextType.TEXT),
                TextNode("End link", TextType.LINK, "https://www.end.com"),
            ],
            new_nodes,
        )

    def test_split_node_links_with_a_mix_of_text_and_non_text_nodes(self):
        nodes = [
            TextNode("This is text with a link [link1](https://www.link1.com)", TextType.TEXT),
            TextNode("This is italic text", TextType.ITALIC),
            TextNode("Another link here [link2](https://www.link2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://www.link1.com"),
                TextNode("This is italic text", TextType.ITALIC),
                TextNode("Another link here ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://www.link2.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_adjacent_links(self):
        node = TextNode(
            "Links: [link1](https://www.link1.com)[link2](https://www.link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://www.link1.com"),
                TextNode("link2", TextType.LINK, "https://www.link2.com"),
            ],
            new_nodes,
        )   

# --------------------------------------------------------------------------
    # This test is commented out because overlapping links are not supported in markdown syntax.

    # def test_split_nodes_link_with_overlapping_links(self):
    #     node = TextNode(
    #         "Check this [link [nested](https://www.nested.com)](https://www.outer.com)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("Check this ", TextType.TEXT),
    #             TextNode("link [nested](https://www.nested.com)", TextType.LINK, "https://www.outer.com"),
    #         ],
    #         new_nodes,
    #     )
# --------------------------------------------------------------------------


# This test is commented out because nested links are not supported in markdown syntax.

    # def test_split_nodes_link_with_nested_links(self):
    #     node = TextNode(
    #         "Check this [link [nested](https://www.nested.com)](https://www.outer.com)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("Check this ", TextType.TEXT),
    #             TextNode("link [nested](https://www.nested.com)", TextType.LINK, "https://www.outer.com"),
    #         ],
    #         new_nodes,
    #     )
# --------------------------------------------------------------------------

    def test_split_nodes_link_with_no_text_between_links(self):
        node = TextNode(
            "[link1](https://www.link1.com)[link2](https://www.link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://www.link1.com"),
                TextNode("link2", TextType.LINK, "https://www.link2.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_special_characters_in_links(self):
        node = TextNode(
            "Check this [link!@#](https://www.example.com/!@#)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("link!@#", TextType.LINK, "https://www.example.com/!@#"),
            ],
            new_nodes,
        )

    
    