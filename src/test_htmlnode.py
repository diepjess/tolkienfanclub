import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            self.assertEqual(str(context), "LeafNode must have a value")

    def test_leaf_node_rejects_children_in_constructor(self):
        with self.assertRaises(TypeError):
            node = LeafNode("p", "paragraph", children=["some child"])

    def test_leaf_node_cannot_add_children(self):
        node = LeafNode("p", "paragraph")
        with self.assertRaises(ValueError) as context:
            node.children = ["some child"]
            self.assertEqual(str(context), "LeafNode cannot have children")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")
        
    def test_leaf_to_html_no_vale(self):
        node = LeafNode("p")
        node_2 = LeafNode("div", "")
        self.assertEqual(node.to_html(), "<p></p>")
        self.assertEqual(node_2.to_html(), "<div></div>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        parent_node = ParentNode("div", [LeafNode("span", "child")])
        test_string = 'ParentNode(div, [LeafNode(span, child, None)], None)'
        self.assertEqual(repr(parent_node), test_string)
    
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2", {"href": "link"})
        child_node3 = LeafNode(None, "Normal")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        test_string = '<div><span>child</span><p href="link">child2</p>Normal</div>'
        self.assertEqual(parent_node.to_html(), test_string)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node_1 = ParentNode("span", [grandchild_node])
        child_node_2 = LeafNode("em", "Italic")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        test_string = "<div><span><b>grandchild</b></span><em>Italic</em></div>"
        self.assertEqual(parent_node.to_html(), test_string)
    
    def test_to_html_invalid_children(self):
        with self.assertRaises(TypeError) as context:
            parent = ParentNode("div", ["text"])
            parent.to_html()
            self.assertEqual(str(context), "All children must be instances of HTMLNode")
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent = ParentNode("div", [child_node])
        with self.assertRaises(ValueError) as context:
            parent.tag = None
            parent.to_html()
            self.assertEqual(str(context), "ParentNode must have a tag")
    
    def test_to_html_no_children(self):
        child_node = LeafNode("span", "child")
        parent = ParentNode("div", [child_node])
        with self.assertRaises(ValueError) as context:
            parent.children = None
            parent.to_html()
            self.assertEqual(str(context), "ParentNode must have at least one child")
    
    def test_to_html_empty_children(self):
        child_node = LeafNode("span", "child")
        parent = ParentNode("div", [child_node])
        with self.assertRaises(ValueError) as context:
            parent.children = []
            parent.to_html()
            self.assertEqual(str(context), "ParentNode must have at least one child")
    
    def test_no_tags(self):
        with self.assertRaises(ValueError) as context:
            child_node = LeafNode("span", "child")
            parent = ParentNode(None, [child_node])
            self.assertEqual(str(context), "ParentNode must have a tag")
    
    def test_no_children(self):
        with self.assertRaises(ValueError) as context:
            parent = ParentNode("div", None)
            self.assertEqual(str(context), "ParentNode must have at least one child")

    def test_empty_childen(self):
        with self.assertRaises(ValueError) as context:
            parent = ParentNode("div", [])
            self.assertEqual(str(context), "ParentNode must have at least one child")

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()