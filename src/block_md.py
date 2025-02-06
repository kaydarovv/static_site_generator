import re

def markdown_to_blocks(markdown: str) -> list:
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

# def block_to_block_type(block: str) -> str:

#     code_pattern = r"^```[\s\S]*?```$"
#     is_code = bool(re.search(code_pattern, block))
#     if is_code:
#         return "code"
    
#     heading_pattern = r"^#{1,6} [^\s]"
#     is_heading = bool(re.search(heading_pattern, block))
#     if is_heading:
#         return "heading"
    
#     quote_pattern = r"^>.*(?:\n>.*)*$"
#     is_quote = bool(re.search(quote_pattern, block))
#     if is_quote:
#         return "quote"
    
#     ordered_list_pattern = r"^1\. .*(?:\n[2-9]\. .*)*$"
#     is_ordered_list = bool(re.search(ordered_list_pattern, block))
#     if is_ordered_list:
#         return "ordered_list"
    
#     unordered_list_pattern = r"^[*-] \S.*(?:\n[*-] \S.*)*$"
#     is_unordered_list =bool(re.search(unordered_list_pattern, block))
#     if is_unordered_list:
#         return "unordered_list"
    
#     return "paragraph"

import re

def block_to_block_type(block: str) -> tuple[str, str]:
    """
    Analyzes a text block and returns its type along with cleaned content.
    
    Args:
        block: Input text block
        
    Returns:
        Tuple containing (block_type, cleaned_block)
    """
    # Code block pattern and cleaning
    code_pattern = r"^```(?:\w+\n)?([\s\S]*?)```$"
    code_match = re.search(code_pattern, block)
    if code_match:
        return "code", code_match.group(1).strip()
    
    # Heading pattern and cleaning
    heading_pattern = r"^(#{1,6})\s+(.+)$"
    heading_match = re.search(heading_pattern, block)
    if heading_match:
        return "heading", heading_match.group(2).strip()
    
    # Quote pattern and cleaning
    quote_pattern = r"^>\s*(.+?)(?:\n>\s*(.+?))*$"
    quote_match = re.search(quote_pattern, block)
    if quote_match:
        cleaned_quote = re.sub(r"^>\s*", "", block, flags=re.MULTILINE)
        return "quote", cleaned_quote.strip()
    
    # Ordered list pattern and cleaning
    ordered_list_pattern = r"^(\d+\.\s+.+?)(?:\n\d+\.\s+.+?)*$"
    ordered_match = re.search(ordered_list_pattern, block)
    if ordered_match:
        cleaned_list = re.sub(r"^\d+\.\s+", "", block, flags=re.MULTILINE)
        return "ordered_list", cleaned_list.strip()
    
    # Unordered list pattern and cleaning
    unordered_list_pattern = r"^([-*]\s+.+?)(?:\n[-*]\s+.+?)*$"
    unordered_match = re.search(unordered_list_pattern, block)
    if unordered_match:
        cleaned_list = re.sub(r"^[-*]\s+", "", block, flags=re.MULTILINE)
        return "unordered_list", cleaned_list.strip()
    
    # Default case: paragraph
    return "paragraph", block.strip()