import unittest

from markdown_parser import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter_bold(self):
        node = TextNode("Text with **bold text** in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_text_1 = TextNode("Text with ", TextType.TEXT)
        node_bold_1 = TextNode("bold text", TextType.BOLD)
        node_text_2 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], node_text_1)
        self.assertEqual(result[1], node_bold_1)
        self.assertEqual(result[2], node_text_2)
    
    def test_single_delimiter_italic(self):
        node = TextNode("Text with _italic text_ in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node_text_1 = TextNode("Text with ", TextType.TEXT)
        node_italic_1 = TextNode("italic text", TextType.ITALIC)
        node_text_2 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], node_text_1)
        self.assertEqual(result[1], node_italic_1)
        self.assertEqual(result[2], node_text_2)

    def test_single_delimiter_code(self):
        node = TextNode("Text with `code` in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        node_text_1 = TextNode("Text with ", TextType.TEXT)
        node_code_1 = TextNode("code", TextType.CODE)
        node_text_2 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], node_text_1)
        self.assertEqual(result[1], node_code_1)
        self.assertEqual(result[2], node_text_2)
    
    def test_multiple_delimiter_bold(self):
        node = TextNode("Text with **bold** and **more bold** formatting", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_text_1 = TextNode("Text with ", TextType.TEXT)
        node_bold_1 = TextNode("bold", TextType.BOLD)
        node_text_2 = TextNode(" and ", TextType.TEXT)
        node_bold_2 = TextNode("more bold", TextType.BOLD)
        node_text_3 = TextNode(" formatting", TextType.TEXT)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], node_text_1)
        self.assertEqual(result[1], node_bold_1)
        self.assertEqual(result[2], node_text_2)
        self.assertEqual(result[3], node_bold_2)
        self.assertEqual(result[4], node_text_3)
    
    def test_plain_text_no_delimiters(self):
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        result_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_italic = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result_code = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result_bold), 1)
        self.assertEqual(len(result_italic), 1)
        self.assertEqual(len(result_code), 1)
        self.assertEqual(node, result_bold[0])
        self.assertEqual(node, result_italic[0])
        self.assertEqual(node, result_code[0])
    
    def test_empty_string_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(node, result[0])
    
    def test_delimiter_at_start_or_end(self):
        node_1 = TextNode("`code` at start", TextType.TEXT)
        node_2 = TextNode("ends with `code`", TextType.TEXT)
        node_code = TextNode("code", TextType.CODE)
        node_start = TextNode(" at start", TextType.TEXT)
        node_end = TextNode("ends with ", TextType.TEXT)
        result_1 = split_nodes_delimiter([node_1], "`", TextType.CODE)
        result_2 = split_nodes_delimiter([node_2], "`", TextType.CODE)
        self.assertEqual(len(result_1), 2)
        self.assertEqual(len(result_2), 2)
        self.assertEqual(result_1, [node_code, node_start])
        self.assertEqual(result_2, [node_end, node_code])
        
    def test_multiple_nodes(self):
        node_1 = TextNode("Text with `code`", TextType.TEXT)
        node_2 = TextNode("Already bold", TextType.BOLD)
        node_3 = TextNode("More `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node_1, node_2, node_3], "`", TextType.CODE)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], TextNode("Text with ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))
        self.assertEqual(result[2], TextNode("Already bold", TextType.BOLD))
        self.assertEqual(result[3], TextNode("More ", TextType.TEXT))
        self.assertEqual(result[4], TextNode("code", TextType.CODE))
        self.assertEqual(result[5], TextNode(" text", TextType.TEXT))
    
    def test_invalid_markdown(self):
        node = TextNode("Text with `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            result = split_nodes_delimiter([node], "`", TextType.CODE)
            self.assertEqual(str(context), "Closing delimiter not found for `")        
        
    def test_adjacent_delimiters(self):
        node = TextNode("Text with **bold****more bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("Text with ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[2], TextNode("more bold", TextType.BOLD))
    
    def test_invalid_text_type(self):
        node = TextNode("Plain text", TextType.TEXT)
        with self.assertRaises(TypeError) as context:
            result = split_nodes_delimiter([node], "#", "heading")
            self.assertEqual(str(context), "text_type must be a valid TextType enum value")

    def test_empty_node_list(self):
        result =  split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()