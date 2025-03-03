class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(
            f'{key}="{value}"'
            for key, value in self.props.items()
        )
    
    def __repr__(self):
        tag = self.tag
        value = self.value
        children = self.children
        props = self.props
        return f"HTMLNode({tag},\n{value},\nchildren: {children},\n{props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")

        super().__init__(tag, children=None, props=props)
        self.value = value
        
        if self.children is not None:
            raise ValueError("LeafNode cannot have children")
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"