from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    """Split TextNodes of type TEXT based on delimiters
    Non-TextNode objects and TextNodes of other types are reserved unchanged.

    Args:
        old_nodes (list): list of objects. Splits TextNodes of TextType.TEXT
        delimiter (str): markdown delimiter (eg. "**" for bold)
        text_type (TextType): TextTypes to generate based on delimiter

    Raises:
        TypeError: Invalid text_types
        Exception: Delimiter with no closing delimiter is unsupported.

    Returns:
        list: Objects, TextNodes, and TextNodes that have been split.
    """
    if not isinstance(text_type, TextType):
        raise TypeError("text_type must be a valid TextType enum value")
    result_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            # for now preserve Non-TextNode ojbects as is
            result_nodes.append(old_node)
        elif old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
        elif old_node.text == "":
            # for now preserve empty text TextNodes that are passed in
            result_nodes.append(old_node)
        else:
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