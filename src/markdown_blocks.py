

def markdown_to_blocks(markdown):
    initial_blocks = markdown.split('\n\n')
    filtered_blocks = []

    for block in initial_blocks:
        cleaned_block = block.strip()
        if cleaned_block:  
            filtered_blocks.append(cleaned_block)

    return filtered_blocks