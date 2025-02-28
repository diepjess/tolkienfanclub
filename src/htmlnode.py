class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
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
        return f"HTMLNode({tag},\n {value},\n {children},\n {props})"