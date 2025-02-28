from enum import Enum


class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, text_node):
        if not isinstance(text_node, TextNode):
            return False
        return (self.text == text_node.text and
                self.text_type == text_node.text_type and
                self.url == text_node.url)
    
    def __repr__(self):
        text = self.text
        text_type = self.text_type.value
        url = self.url
        return f"TextNode({text}, {text_type}, {url})"