from enum import Enum
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    initial_blocks = markdown.split('\n\n')
    filtered_blocks = []

    for block in initial_blocks:
        cleaned_block = block.strip()
        if cleaned_block:  
            filtered_blocks.append(cleaned_block)

    return filtered_blocks

def block_to_block_type(block):
    # Check for heading (1-6 # characters, followed by space)
    heading_prefixes = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    if block.startswith(heading_prefixes):
        return BlockType.HEADING
    
    # Check for code block (starts with ''' and new line, ends with ''')   
    lines = block.split('\n')
    if len(lines) > 1 and lines[0] == ("```") and lines[-1] == ("```"):
        return BlockType.CODE

    ## code_block_prefix = ("```\n")
    ## if block.startswith(code_block_prefix) and block.endswith("```"):
    ##     return BlockType.CODE

    # Check for quote block (every line starts with >)
    lines = block.split("\n")
    is_quote = True

    for line in lines:
        leading_white_spaces_stripped_line = line.lstrip()
        if leading_white_spaces_stripped_line:
            first_non_space_character = leading_white_spaces_stripped_line[0]
        
            if first_non_space_character != ">":
                is_quote = False
                break
        
        else:
            is_quote = False
            break
  
    if is_quote:
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    lines = block.split("\n")
        
    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST

    # Check for ordered list (every line starts with "1. 2. 3. and so on")
    lines = block.split("\n")

    count = 1

    for line in lines:
        if not line.startswith(f"{count}. "):
            break
        count += 1
    else:
        return BlockType.ORDERED_LIST

    """
    Code Draft - 1 
    count = 1
    is_ordered_list = True

    for line in lines:
        if line.startswith(f"{count}. "):
            count += 1
            continue
        else:
            is_ordered_list = False
            break

    if is_ordered_list:
        return BlockType.ORDERED_LIST
 """
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        block_node = block_to_html_node(block)
        children.append(block_node)

    return ParentNode(tag="div", children=children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children.append(child)
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type is BlockType.PARAGRAPH:
        cleaned_block = ' '.join(block.split())
        children = text_to_children(cleaned_block)
        return ParentNode(tag="p", children=children)
    
    elif block_type is BlockType.HEADING:
        heading_level = 0
    
        for char in block:
            if char == "#":
                heading_level += 1
            else:
                break

        text = block.lstrip('# ')
        children = text_to_children(text)
        return ParentNode(tag="h" + str(heading_level), children=children)
                        
    elif block_type is BlockType.QUOTE:
        # # remove leading '> ' from each line and join
        # text = quote_text_from_block(block)
        # children = text_to_children(text)
        # return HTMLNode(tag="blockquote", children=children)

        lines = block.splitlines()
        cleaned_lines = []
        for line in lines:
            # lstrip("> ") removes leading '>' and spaces
            cleaned_lines.append(line.lstrip("> ").strip())

        final_output = " ".join(cleaned_lines)
        
        children = text_to_children(final_output)
        return ParentNode(tag="blockquote", children=children)

    elif block_type is BlockType.UNORDERED_LIST:
        li_nodes = []
        
        lines = block.splitlines()

        for line in lines:
            cleaned_text = line[2:]
            child_html_nodes = text_to_children(cleaned_text)
            li_node = ParentNode("li", child_html_nodes)
            li_nodes.append(li_node)

        return ParentNode(tag="ul", children=li_nodes)

    elif block_type is BlockType.ORDERED_LIST:
        li_nodes = []

        lines = block.strip().split('\n')
        for line in lines:

            cleaned_text = line.split(". ", 1)[-1]
            child_html_nodes = text_to_children(cleaned_text)
            li_node = ParentNode("li", child_html_nodes)
            li_nodes.append(li_node)

        return ParentNode(tag="ol", children=li_nodes)

    elif block_type is BlockType.CODE:
        cleaned_block = block[4: -3]

        content_text_node = TextNode(cleaned_block, text_type=TextType.TEXT)

        content_html_node = [text_node_to_html_node(content_text_node)]

        code_parent_node = ParentNode(tag="code", children=content_html_node)

        pre_parent_node = ParentNode(tag="pre", children=[code_parent_node])

        return pre_parent_node
