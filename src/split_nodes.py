from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
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