import unittest
from split_message import split_message, MessageSplitError


class TestSplitMessage(unittest.TestCase):
    def test_element_too_long(self):
        html = "<p>" + "A" * 5000 + "</p>"

        with self.assertRaises(MessageSplitError) as context:
            list(split_message(html, max_len=4096))

        self.assertIn("Элемент слишком длинный", str(context.exception))
        self.assertIn("для одного фрагмента", str(context.exception))

    def test_long_text(self):
        html = "<p>" + "A" * 5000 + "</p>"
        with self.assertRaises(MessageSplitError):
            list(split_message(html, max_len=4096))

    def test_split_simple(self):
        html = "<p>" + "A" * 3000 + "</p><p>" + "B" * 2000 + "</p>"
        fragments = list(split_message(html, max_len=4096))
        self.assertEqual(len(fragments), 2)
        self.assertTrue(fragments[0].endswith("</p>"))
        self.assertTrue(fragments[1].startswith("<p>"))

    def test_split_with_long_element(self):
        html = "<p>" + "A" * 5000 + "</p><p>" + "B" * 2000 + "</p>"
        with self.assertRaises(MessageSplitError):
            list(split_message(html, max_len=4096))

    def test_split_with_empty_tags(self):
        html = "<p></p><p>" + "A" * 3000 + "</p><p>" + "B" * 1000 + "</p>"
        fragments = list(split_message(html, max_len=3500))
        self.assertEqual(len(fragments), 2)
        self.assertTrue(fragments[0].endswith("</p>"))
        self.assertTrue(fragments[1].startswith("<p>"))


if __name__ == '__main__':
    unittest.main()
