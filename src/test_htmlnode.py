import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
            None,
            None
        )
        self.assertEqual("div", node.tag)
        self.assertEqual("I wish I could read", node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)
    
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "This is a html node")
        self.assertEqual("", node.props_to_html())
    
    def test_props_to_html_dict1(self):
        node = HTMLNode(
            "p",
            "This is a html node",
            None,
            {
                "href": "https://www.google.com",
            }
        )
        test_string = ' href="https://www.google.com"'
        self.assertEqual(test_string, node.props_to_html())
    
    def test_props_to_html_dict2(self):
        node = HTMLNode(
            "p",
            "This is a html node",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        test_string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test_string, node.props_to_html())
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "This is a html node",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        test_string = "HTMLNode(p,\nThis is a html node,\nchildren: None,\n"
        test_string += "{'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(test_string, repr(node))


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("html", None)
            self.assertEqual(str(context.exception), "LeafNode must have a value")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")


if __name__ == "__main__":
    unittest.main()