from textnode import TextNode, TextType


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
    


if __name__=="__main__":
    main()