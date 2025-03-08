import unittest

from markdown_parser import (
    split_nodes_delimiter,
    split_nodes_image,
    extract_markdown_images, 
    extract_markdown_links,
    )

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter_bold(self):
        node = TextNode("Text with **bold text** in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" in it", TextType.TEXT),
            ]
        )
    
    def test_single_delimiter_italic(self):
        node = TextNode("Text with _italic text_ in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" in it", TextType.TEXT),
            ]
        )

    def test_single_delimiter_code(self):
        node = TextNode("Text with `code` in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" in it", TextType.TEXT),
            ]
        )
    
    def test_multiple_delimiter_bold(self):
        node = TextNode("Text with **bold** and **more bold** formatting", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
                TextNode(" formatting", TextType.TEXT),
            ]
        )
    
    def test_plain_text_no_delimiters(self):
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        result_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        result_italic = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result_code = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(result_bold, [node])
        self.assertListEqual(result_italic, [node])
        self.assertListEqual(result_code, [node])
    
    def test_empty_string_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(result, [node])
    
    def test_delimiter_at_start_or_end(self):
        node_1 = TextNode("`code` at start", TextType.TEXT)
        node_2 = TextNode("ends with `code`", TextType.TEXT)
        result_start = split_nodes_delimiter([node_1], "`", TextType.CODE)
        result_end = split_nodes_delimiter([node_2], "`", TextType.CODE)
        self.assertListEqual(
            result_start,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at start", TextType.TEXT),
            ]
        )
        self.assertListEqual(
            result_end,
            [
                TextNode("ends with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )
        
    def test_multiple_nodes(self):
        node_1 = TextNode("Text with `code`", TextType.TEXT)
        node_2 = TextNode("Already bold", TextType.BOLD)
        node_3 = TextNode("More `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node_1, node_2, node_3], "`", TextType.CODE)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("Already bold", TextType.BOLD),
                TextNode("More ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    def test_invalid_markdown(self):
        node = TextNode("Text with `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            result = split_nodes_delimiter([node], "`", TextType.CODE)
            self.assertEqual(str(context), "Closing delimiter not found for `")        
        
    def test_adjacent_delimiters(self):
        node = TextNode("Text with **bold****more bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("more bold", TextType.BOLD),
            ]
        )
    
    def test_invalid_text_type(self):
        node = TextNode("Plain text", TextType.TEXT)
        with self.assertRaises(TypeError) as context:
            result = split_nodes_delimiter([node], "#", "heading")
            self.assertEqual(str(context), "text_type must be a valid TextType enum value")

    def test_empty_node_list(self):
        result =  split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertListEqual(result, [])


class TestExtractMarkdownImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [("image", "https://i.imgur.com/zjjcJKZ.png")], 
        )
    
    def test_extract_multi_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        text += ". This is some more ![image2](image.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "image.jpeg"),
            ]
        )
    
    def test_extract_plain_text(self):
        self.assertListEqual([], extract_markdown_images("No images here!"))
    
    def test_extract_empty_text(self):
        self.assertListEqual([], extract_markdown_images(""))
    
    def test_extract_image_special_chars(self):
        text = "![My cool image!](https://example.com/img?id=123&size=large)"
        expected = [("My cool image!", "https://example.com/img?id=123&size=large")]
        self.assertListEqual(expected, extract_markdown_images(text))
    
    def test_extract_mixed_content(self):
        text = "This is text with a [link](urllink) and ![image](image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [("image", "image.png")])


class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_markdown_link(self):
        text = "This is text with a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
            [("link", "https://boot.dev")], 
        )
    
    def test_extract_multi_markdown_link(self):
        text = "This is text with a [link](https://boot.dev) and [other](https://google.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
            [
                ("link", "https://boot.dev"),
                ("other", "https://google.com"),
            ]
        )
    
    def test_extract_plain_text(self):
        self.assertListEqual([], extract_markdown_links("No images here!"))
    
    def test_extract_empty_text(self):
        self.assertListEqual([], extract_markdown_links(""))
    
    def test_extract_link_special_chars(self):
        text = "[My cool link!](https://example.com/img?id=123&size=large)"
        expected = [("My cool link!", "https://example.com/img?id=123&size=large")]
        self.assertListEqual(expected, extract_markdown_links(text))
    
    def test_extract_mixed_content(self):
        text = "This is text with a [link](urllink) and ![image](image.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("link", "urllink")])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multi_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_no_image(self):
        node = TextNode("This is a text with no image!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a text with no image!", TextType.TEXT),
            ]
        )
    
    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("", TextType.TEXT)])
    
    def test_content_is_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_adjacent_images(self):
        node = TextNode("![image1](imagelink1)![image2](imagelink2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "imagelink1"),
                TextNode("image2", TextType.IMAGE, "imagelink2"),
            ],
            new_nodes,
        )
    
    def test_whitespace_around_image(self):
        node = TextNode(" ![image](imageurl) ", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "imageurl"),
                TextNode(" ", TextType.TEXT),
            ],
            new_nodes,
        )
    
    # TODO: implment the following test
    # mixed content (links and images)
    # Broken links (incomplete or malformed markdown)
    # multiple nodes (like say text only, contains image, contains link)


if __name__ == "__main__":
    unittest.main()