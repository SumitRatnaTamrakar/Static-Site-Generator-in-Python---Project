from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
                new_nodes.append(node)
        
        else:
            new_nodes.extend(
                split_node_by_delimiter(node, delimiter, text_type)
            )
    return new_nodes

def split_node_by_delimiter(node, delimiter, text_type):
    text = node.text
    new_nodes = []

    count = text.count(delimiter)
    if count % 2 != 0:
        raise ValueError("Unmatched delimiter in text")

    parts = text.split(delimiter)

    for i, part in enumerate(parts):
        if part == "":
            continue  # skip empty pieces

    # for i, part in enumerate(parts):
        node_type = TextType.TEXT if i % 2 == 0 else text_type
        new_nodes.append(TextNode(part, node_type))

        # if i % 2 == 0:
        #     # outside delimiters
        #     node_type = TextType.TEXT
        # else:
        #     # inside delimiters
        #     node_type = text_type

        # new_nodes.append(TextNode(part, node_type))

    return new_nodes

# Regex patterns for inline elements

# -----------------------------------------------------------------------
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
# -----------------------------------------------------------------------

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

# -----------------------------------------------------------------------
# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# print(extract_markdown_links(text))
# # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
# -----------------------------------------------------------------------

def extract_markdown_links(text):
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

# -----------------------------------------------------------------------

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        # If there are no images, keep the node as is
        if not images:
            new_nodes.append(node)
            continue

        # Process each image found in the text
        current_index = 0

        for alt_text, url in images:
            pattern = f"![{alt_text}]({url})"

            # Find this pattern in full text, starting after last match
            image_start = text.find(pattern, current_index)
            if image_start == -1:
                continue
            image_end = image_start + len(pattern)

            # Text before the image
            if current_index < image_start:
                before = text[current_index: image_start]
                new_nodes.append(TextNode(before, TextType.TEXT))

            # The image node iteself
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Move index to after this image
            current_index = image_end
        
        # Leftover text after last image

        if current_index < len(text):
            after = text[current_index: len(text)]
            new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes

# ------------------------------------------------

# Old code

# def split_nodes_image(old_nodes):
    # new_nodes = []

    # for node in old_nodes:
    #     if node.text_type is not TextType.TEXT:
    #         new_nodes.append(node)
    #         continue

    #     text = node.text
    #     images = extract_markdown_images(text)

    #     # If there are no images, keep the node as is
    #     if not images:
    #         new_nodes.append(node)
    #         continue

        # # Process each image found in the text
        # current_index = 0

        # for alt_text, url in images:
        #     parts = text.split(f"![{alt_text}]({url})", 1)
        #     before_image = parts[0]
        #     after_image = parts[1] if len(parts) > 1 else ""

        #     if before_image:
        #         new_nodes.append(TextNode(before_image, TextType.TEXT))

        #     new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        #     text = after_image  # Update text to the remaining part

        # if text:
        #     new_nodes.append(TextNode(text, TextType.TEXT))

    # return new_nodes

# -----------------------------------------------------------------------

# node = TextNode(
#     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#     TextType.TEXT,
# )
# new_nodes = split_nodes_link([node])
# # [
# #     TextNode("This is text with a link ", TextType.TEXT),
# #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
# #     TextNode(" and ", TextType.TEXT),
# #     TextNode(
# #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
# #     ),
# # ]

# -----------------------------------------------------------------------

# Old code

# def split_nodes_link(old_nodes):
#     new_nodes = []

#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue

#         current_text = node.text
#         links = extract_markdown_links(current_text)

#         if not links:
#             new_nodes.append(node)
#             continue

#         current_index = 0

#         for link_text, link_url in links:
#             markdown = f"[{link_text}]({link_url})"
#             link_start = current_text.find(markdown, current_index)
#             if link_start == -1:
#                 continue  # should not happen
#             link_end = link_start + len(markdown)

#             # Text before the link
#             if current_index < link_start:
#                 before_link = current_text[current_index:link_start]
#                 new_nodes.append(TextNode(before_link, TextType.TEXT))

#             # The link itself
#             new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

#             # Move past this link
#             current_index = link_end

#         # Any remaining text after the last link
#         if current_index < len(current_text):
#             after_link = current_text[current_index:]
#             if after_link:
#                 new_nodes.append(TextNode(after_link, TextType.TEXT))

#     return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        current_index = 0

        for label, url in links:
            pattern = f"[{label}]({url})"

            link_start = text.find(pattern,current_index)
            if link_start == -1:
                continue
            link_end = link_start + len(pattern)

            #text before the link
            if current_index < link_start:
                before = text[current_index: link_start]
                new_nodes.append(TextNode(before, TextType.TEXT))

            # the link node
            new_nodes.append(TextNode(label, TextType.LINK, url))

            current_index = link_end

        # leftover text after last link
        if current_index < len(text):
            after = text[current_index: len(text)]
            new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes

# -------------------------------------------------

def text_to_textnodes(text):

    # 1. Start with a single TEXT node
    nodes = [ TextNode(text, TextType.TEXT) ]

    # 2. Split by bold marker
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # 3. Split by italic markers
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # 4. Split by code marker
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # 5. Split out image nodes
    nodes = split_nodes_image(nodes)

    # 6. Split out link nodes
    nodes = split_nodes_link(nodes)

    # 7. Return final list of nodes
    return nodes
