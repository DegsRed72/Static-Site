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
        if self.value == "" or self.value == None:
            raise ValueError("All leafnodes must have a value")
        
        if self.tag == "" or self.tag == None:
            return self.value
        if self.props == None:
            html_render = f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            html_render = f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

        return html_render
        
