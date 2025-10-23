from textnode import *
import re

def text_to_textnode(text):
    new_text_nodes = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "**", TextType.BOLD)
    new_text_nodes = split_nodes_delimiter(new_text_nodes, "_", TextType.ITALIC)
    new_text_nodes = split_nodes_delimiter(new_text_nodes, "`", TextType.CODE)
    new_text_nodes = split_nodes_image(new_text_nodes)
    new_text_nodes = split_nodes_link(new_text_nodes)
    return new_text_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type != TextType.PLAIN:
                new_nodes.append(node)
            else: 
                new_nodes.extend(split_into_TextNodes(node, delimiter, text_type))
        else:
            raise Exception("node is not TextNode")
    return new_nodes

def split_into_TextNodes(node, delimiter, text_type):
    new_nodes = []
    if check_correct_delimiter(delimiter, text_type):
        split_nodes = node.text.split(delimiter)
    if len(split_nodes) % 2 == 0:
        raise Exception("Incorrect markdown format: the delimiter must surround the text")
    elif len(split_nodes) == 1:
        return [node]
    for i in range(len(split_nodes)):  
        if i % 2 == 0:
            new_nodes.append(TextNode(split_nodes[i], TextType.PLAIN))
        else:
            new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def check_correct_delimiter(delimiter, text_type):
    match delimiter:
        case "**":
            return text_type == TextType.BOLD
        case "_":
            return text_type == TextType.ITALIC
        case "`":
            return text_type == TextType.CODE
        case _:
            raise Exception("Invalid delimiter (must be '**', '_', or '`')")
        
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if not extract_markdown_images(node.text):
                new_nodes.append(node)
            else:
                for i in range(0, len(extract_markdown_images(node.text))):
                    image_alt, image_link = extract_markdown_images(node.text)[i]
                    if i == 0:
                        sections = node.text.split(f"![{image_alt}]({image_link})", 1)
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                        if i == len(extract_markdown_images(node.text)) - 1 and sections[i + 1]:
                            new_nodes.append(TextNode(sections[i + 1], TextType.PLAIN))                        
                    else:
                        sections.extend(sections[i].split(f"![{image_alt}]({image_link})", 1))
                        del(sections[i])
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                        if i == len(extract_markdown_images(node.text)) - 1 and sections[i + 1]:
                            new_nodes.append(TextNode(sections[i + 1], TextType.PLAIN))                      
        else:
            raise Exception("Not a TextNode")
                
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if not extract_markdown_links(node.text):
                new_nodes.append(node)
            else:
                for i in range(0, len(extract_markdown_links(node.text))):
                    anchor_text, url = extract_markdown_links(node.text)[i]
                    if i == 0:
                        sections = node.text.split(f"[{anchor_text}]({url})", 1)
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                        new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                        if i == len(extract_markdown_images(node.text)) - 1 and sections[i + 1]:
                            new_nodes.append(TextNode(sections[i + 1], TextType.PLAIN))
                    else:
                        sections.extend(sections[i].split(f"[{anchor_text}]({url})", 1))
                        del(sections[i])
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                        new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                        if i == len(extract_markdown_images(node.text)) - 1 and sections[i + 1]:
                            new_nodes.append(TextNode(sections[i + 1], TextType.PLAIN))                   
        else:
            raise Exception("Not a TextNode")
                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
