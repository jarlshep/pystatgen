import re
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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        original_text = old_node.text
        image_list = extract_markdown_images(original_text)
        
        if len(image_list) == 0:
            node_list.append(old_node)
            continue
        
        for image in image_list:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            if sections[0] != "":
                node_list.append(TextNode(sections[0], TextType.TEXT))
            node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        
        if original_text != "":
            node_list.append(TextNode(original_text, TextType.TEXT))
        
    return node_list

def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue
        
        original_text = old_node.text
        link_list = extract_markdown_links(original_text)
        
        if len(link_list) == 0:
            node_list.append(old_node)
            continue

        for link in link_list:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: link section not closed")
            if sections[0] != "":
                node_list.append(TextNode(sections[0], TextType.TEXT))
            node_list.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            node_list.append(TextNode(original_text, TextType.TEXT))
        
    return node_list

def text_to_textnodes(text):
    
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)

    return node_list


