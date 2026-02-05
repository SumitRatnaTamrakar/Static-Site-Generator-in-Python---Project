from enum import Enum

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