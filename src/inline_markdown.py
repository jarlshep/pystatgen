from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != text_type.TEXT:
            node_list.append(node)
            continue
        textnode_list = []
        delimited_list = node.text.split(delimiter)
        if len(delimited_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(delimited_list)):
            if delimited_list[i] == "":
                continue
            if i % 2 == 0:
                textnode_list.append(TextNode(delimited_list[i], text_type.TEXT))
            else:
                textnode_list.append(TextNode(delimited_list[i], text_type))
        node_list.extend(textnode_list)
    return node_list




