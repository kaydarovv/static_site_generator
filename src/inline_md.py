import re

from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("there is a missing closing delimiter")
        
        lst = node.text.split(delimiter)
        for i in range(0, len(lst)):
            if i % 2 == 0:
                new_node = TextNode(lst[i], text_type = TextType.TEXT)
            else:
                new_node = TextNode(lst[i], text_type = text_type)
            lst[i] = new_node
        new_nodes.extend(lst)
             
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        image_list = extract_markdown_images(node.text)

        if not image_list:
            new_nodes.append(node)
            continue

        raw_text = node.text
        for image_data in image_list:
            image_alt = image_data[0]
            image_url = image_data[1]
            
            temp_text_list = raw_text.split(f"![{image_alt}]({image_url})", 1)

            if temp_text_list[0]:
                new_text_node = TextNode(temp_text_list[0], text_type = node.text_type)
                new_nodes.append(new_text_node)
            new_image_node = TextNode(text=image_alt, text_type=TextType.IMAGE, url=image_url)
            new_nodes.append(new_image_node)
            raw_text = temp_text_list[-1]
        if raw_text:
            new_text_node = TextNode(raw_text, text_type = node.text_type)
            new_nodes.append(new_text_node)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        link_list = extract_markdown_links(node.text)

        if not link_list:
            new_nodes.append(node)
            continue

        raw_text = node.text
        for link_data in link_list:
            anchor_text = link_data[0]
            link_url = link_data[1]
            
            temp_text_list = raw_text.split(f"[{anchor_text}]({link_url})", 1)

            if temp_text_list[0]:
                new_text_node = TextNode(temp_text_list[0], text_type = node.text_type)
                new_nodes.append(new_text_node)
            new_link_node = TextNode(text=anchor_text, text_type=TextType.LINK, url=link_url)
            new_nodes.append(new_link_node)
            raw_text = temp_text_list[-1]
        if raw_text:
            new_text_node = TextNode(raw_text, text_type = node.text_type)
            new_nodes.append(new_text_node)

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    parsing_sequence = [
        (split_nodes_image, None),
        (split_nodes_link, None),
        (split_nodes_delimiter, ("`", TextType.CODE)),
        (split_nodes_delimiter, ("**", TextType.BOLD)),
        (split_nodes_delimiter, ("*", TextType.ITALIC))
    ]
    node = TextNode(text, TextType.TEXT)
    result = [node]
    for parser_func, args in parsing_sequence:
        if args is None:
            result = parser_func(result)
        else:
            delimiter, text_type = args
            result = parser_func(result, delimiter, text_type)
            
    return result