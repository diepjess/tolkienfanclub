import unittest

from converter import text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
    
    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None)
    
    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props["href"], "google.com")
        self.assertEqual(len(html_node.props), 1)
    
    def test_image(self):
        node = TextNode("Cool image", TextType.IMAGE, "imageurl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "imageurl")
        self.assertEqual(html_node.props["alt"], "Cool image")
        self.assertEqual(len(html_node.props), 2)
    
    def test_converter_not_text_node(self):
        not_node = ""
        with self.assertRaises(TypeError) as context:
            html_node = text_node_to_html_node(not_node)
            self.assertEqual(str(context), "Expected a TextNode object")
    
    def test_converter_invalid_text_type(self):
        invalid_node = TextNode("This is a node", TextType.TEXT)
        invalid_node.text_type = "invalid"
        with self.assertRaises(ValueError) as context:
            html_node = text_node_to_html_node(invalid_node)
            self.assertEqual(str(context), "Invalid text type: invalid")
    
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, None)
        
    def test_special_characters(self):
        text = "Text with <special> & characters"
        node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, text)
    
    def test_link_empty_url(self):
        node = TextNode("Click me!", TextType.LINK, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props["href"], "")
    
    def test_image_empty_url(self):
        node = TextNode("Cool image", TextType.IMAGE, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "")
        self.assertEqual(html_node.props["alt"], "Cool image")


if __name__ == "__main__":
    unittest.main()