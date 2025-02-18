from .htmlnode import HTMLNode, ParentNode
from .textnode import text_node_to_html_node
from .block_md import markdown_to_blocks, block_to_block_type
from .inline_md import text_to_textnodes

def block_to_html_nodes(block: str, block_type: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    if not markdown:
        raise Exception("Do not enter empty markdown")
    html = ParentNode(tag="div", children=[])

    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        block_type, clean_block = block_to_block_type(block)
        match block_type:
            case "code":
                code_node = ParentNode(tag="code", children=[])
                code_node.children = block_to_html_nodes(clean_block, block_type)
                html_block = ParentNode(tag="pre", children=[code_node])

            case "heading":
                lvl = len(block) - len(block.lstrip("#"))
                html_block = ParentNode(tag=f"h{lvl}", children=[])
                html_block.children = block_to_html_nodes(clean_block, block_type)

            case "quote":
                html_block = ParentNode(tag="blockquote", children=[])
                html_block.children = block_to_html_nodes(clean_block, block_type)

            case "ordered_list":
                html_block = ParentNode(tag="ol", children=[])  
                items = clean_block.split("\n")
                for item in items:
                    li_node = ParentNode(tag="li", children=[])  
                    li_node.children = block_to_html_nodes(item, block_type)
                    html_block.children.append(li_node)

            case "unordered_list":
                html_block = ParentNode(tag="ul", children=[]) 
                items = clean_block.split("\n")
                for item in items:
                    li_node = ParentNode(tag="li", children=[])  
                    li_node.children = block_to_html_nodes(item, block_type)
                    html_block.children.append(li_node)

            case "paragraph":
                html_block = ParentNode(tag="p", children=[])
                html_block.children = block_to_html_nodes(clean_block, block_type)

        html.children.append(html_block)
    
    return html

