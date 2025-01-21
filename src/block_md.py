import re

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    current_block = []
    blocks = []
    
    for line in lines:
        if line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block))
            current_block = []
        else:
            current_block.append(line)
            
    if current_block:
                blocks.append("\n".join(current_block))
    return blocks

def block_to_block_type(block: str) -> str:
    code_pattern = r"^```[\s\S]*?```$"
    is_code = bool(re.search(code_pattern, block))

    heading_pattern = r"^#{1,6} [^\s]"
    is_heading = bool(re.search(heading_pattern, block))
    
    quote_pattern = r"^>.*(?:\n>.*)*$"
    is_quote = bool(re.search(quote_pattern, block))

    ordered_list_pattern = r"^1\. .*(?:\n[2-9]\. .*)*$"
    is_ordered_list = bool(re.search(ordered_list_pattern, block))
    unordered_list_pattern = r"^[*-] \S.*(?:\n[*-] \S.*)*$"
    is_unordered_list =bool(re.search(unordered_list_pattern, block))

    if is_code:
        return "code"
    elif is_heading:
        return "heading"
    elif is_quote:
        return "quote"
    elif is_ordered_list:
        return "ordered_list"
    elif is_unordered_list:
        return "unordered_list"
    else:
        return "paragraph"