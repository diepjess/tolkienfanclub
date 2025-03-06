from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode object")

    handlers = {
        TextType.TEXT: lambda node: LeafNode(None, node.text),
        TextType.BOLD: lambda node: LeafNode("b", node.text),
        TextType.ITALIC: lambda node: LeafNode("i", node.text),
        TextType.CODE: lambda node: LeafNode("code", node.text),
        TextType.LINK: lambda node: LeafNode("a", node.text, {"href": node.url}),
        TextType.IMAGE: lambda node: LeafNode("img", "", {"src": node.url, "alt": node.text}),
    }
    
    if text_node.text_type not in handlers:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    
    return handlers[text_node.text_type](text_node)


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    result_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise ValueError("Expected a TextNode object")
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
        current_text = old_node.text
        while delimiter in current_text:
            parts = current_text.split(delimiter, maxsplit=1)
            before = parts[0]
            rest = parts[1]
            
            if delimiter not in rest:
                raise Exception(f"Closing delimiter not found for {delimiter}")
                
            inner_parts = rest.split(delimiter, maxsplit=1)
            inner = inner_parts[0]
            if len(inner_parts) > 1:
                after = inner_parts[1]
            else:
                after = ""
            
            # design decision to not create empty TextNodes
            if before:
                result_nodes.append(TextNode(before, TextType.TEXT))
            result_nodes.append(TextNode(inner, text_type))
            
            current_text = after

        # design decision to not create empty TextNodes
        if current_text:
            result_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return result_nodes