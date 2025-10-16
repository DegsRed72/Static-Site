from textnode import *

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

