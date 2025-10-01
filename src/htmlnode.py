"""
tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
children - A list of HTMLNode objects representing the children of this node
props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
"""
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        message = ""
        for prop in self.props:
            message = message + f' {prop}="{self.props[prop]}"'
        return message
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        html_render = ""
        if not self.value:
            raise ValueError("All leafnodes must have a value")
        
        if not self.tag:
            return self.value
        if not self.props:
            html_render = f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            html_render = f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

        return html_render
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        html_render = ""
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        
        if not self.children:
            raise ValueError("ChildNode must have a value")
        
        for child in self.children:
            html_part = child.to_html()
            html_render = html_render + html_part
        
        if not self.props:
            return f"<{self.tag}>{html_render}</{self.tag}>"
        else:
            return f"<{self.tag}{super().props_to_html()}>{html_render}</{self.tag}>"

