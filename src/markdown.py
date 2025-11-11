from textnode import *
from htmlnode import LeafNode, HTMLNode, ParentNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    formatted_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            formatted_blocks.append(block)
    return formatted_blocks

def block_to_blocktype(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif check_quotes(markdown):
        return BlockType.QUOTE
    elif check_unordered_list(markdown):
        return BlockType.UNORDERED_LIST
    elif check_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
        
def check_quotes(text):
    split_lines = text.split("\n")
    for line in split_lines:
        if not line.startswith(">"):
            return False
    return True

def check_unordered_list(text):
    split_lines = text.split("\n")
    for line in split_lines:
        if not line.startswith("- "):
            return False
    return True   
 
def check_ordered_list(text):
    if text[0] == "1":
        split_lines = text.split("\n")
        count = 1
        for line in split_lines:
            if len(line) >= 3:
                if line[0] == "0":
                    return False
                prefix = ""
                next_two = ""
                for c in line:
                    if c.isdigit():
                        prefix += f"{c}"
                    else:
                        break
                for c in line:
                    if not c.isdigit():
                        if len(next_two) < 2:
                            next_two += f"{c}"

                if int(prefix) != count or next_two != ". ":
                    return False
                else:
                    count += 1
        
        return True
    else:
        return False
    
def markdown_to_html_node(markdown):
    if not markdown:
        raise Exception("No markdown")
    div_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_blocktype(block)        
        node = None
        match type:
            case BlockType.PARAGRAPH:
                block = " ".join(block.splitlines()).strip() 
                node = create_paragraph_node()
                node.children = text_to_children(block)
            case BlockType.HEADING:
                node = create_heading_node(block)
                block = block.lstrip("# ")
                node.children = text_to_children(block)
            case BlockType.CODE:
                node = create_code_node()
                block = block.strip("```")
                block = block.splitlines()
                block = "\n".join(block)
                block = block.lstrip("\n")
                block += "\n"
                node.children = [TextNode.text_node_to_html_node(TextNode(block, TextType.CODE))]
            case BlockType.QUOTE:
                node = create_quote_node()
                block = block.lstrip("> ")
                node.children = text_to_children(block)
            case BlockType.UNORDERED_LIST:
                node = create_unordered_list_node()
                items = block.splitlines()
                list_nodes = []
                for item in items:
                    if len(item) > 1:
                        item = item.lstrip("- ")
                        list_node = create_list_node()
                        list_node.children = text_to_children(item)
                        list_nodes.append(list_node)
                node.children = list_nodes
            case BlockType.ORDERED_LIST:
                node = create_ordered_list_node()
                items = block.splitlines()
                list_nodes = []
                count = 0
                for item in items:
                    if len(item) > 1:
                        count += 1
                        item = item.lstrip(f"{count}. ")
                        list_node = create_list_node()
                        list_node.children = text_to_children(item)
                        list_nodes.append(list_node)
                node.children = list_nodes
            case _:
                raise Exception("Invalid BlockType")
        div_node.children.append(node)
    return div_node

def create_paragraph_node():
    return ParentNode("p", None)

def create_heading_node(text):
    count = 0
    for c in text:
        if c == "#":
            count += 1
    return ParentNode(f"h{count}", None)
        

def create_code_node():
    return ParentNode("pre", None)

def create_quote_node():
    return ParentNode("blockquote", None)

def create_unordered_list_node():
    return ParentNode("ul", None)

def create_ordered_list_node():
    return ParentNode("ol", None)

def create_list_node():
    return ParentNode("li", None)

def text_to_children(text):
    children = []
    text_nodes = text_to_textnode(text)
    for node in text_nodes:
        children.append(TextNode.text_node_to_html_node(node))
    return children