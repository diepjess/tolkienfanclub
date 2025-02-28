import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):    
    def test_eq_empty_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", 
                         TextType.LINK, 
                         "https://www.boot.dev")
        node2 = TextNode("This is a text node", 
                         TextType.LINK, 
                         "https://www.boot.dev")
        self.assertEqual(node1, node2)
    
    def test_eq_false_diff_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a differnt text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_eq_false_diff_text_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_eq_false_diff_url(self):
        node1 = TextNode("This is a text node", 
                         TextType.LINK, 
                         "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)
    
    def test_eq_false_diff_url2(self):
        node1 = TextNode("This is a text node", 
                         TextType.LINK, 
                         "https://www.boot.dev")
        node2 = TextNode("This is a text node", 
                         TextType.LINK,
                         "http://www.boot.dev")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", 
                         TextType.LINK,
                         "https://www.boot.dev")
        string = "TextNode(This is a text node, link, https://www.boot.dev)"
        self.assertEqual(string, repr(node))


if __name__ == "__main__":
    unittest.main()