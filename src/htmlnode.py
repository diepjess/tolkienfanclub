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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have at least one child")
        if not all(isinstance(child, HTMLNode) for child in children):
            raise TypeError("All children must be instances of HTMLNode")
        
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one child")
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        child_html = list(map(lambda child: child.to_html(), self.children))
        inner_html = "".join(child_html)
        return opening_tag + inner_html + closing_tag
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"