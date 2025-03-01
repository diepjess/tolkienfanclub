import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()