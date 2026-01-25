from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
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

        if i % 2 == 0:
            # outside delimiters
            node_type = TextType.TEXT
        else:
            # inside delimiters
            node_type = text_type

        new_nodes.append(TextNode(part, node_type))

    return new_nodes

