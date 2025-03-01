from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    node1 = TextNode("This is a text node", 
                     TextType.LINK, 
                     "https://www.boot.dev)")
    node2 = TextNode("This is a text node", 
                     TextType.LINK, 
                     "https://www.boot.dev)")
    node3 = TextNode("This is bold text", TextType.BOLD)
    
    print(repr(node1))
    print(repr(node2))
    print(repr(node3))
    print(node1 == node2)
    print(node1 == node3)
    
    node_html = HTMLNode("p",
                        "This is a html node",
                        None,
                        {
                            "href": "https://www.google.com",
                            "target": "_blank"
                        }
                        )
    print(repr(node_html))
    


if __name__=="__main__":
    main()