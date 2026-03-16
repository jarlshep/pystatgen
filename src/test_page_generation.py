import unittest

from page_generation import extract_title, generate_page

class TestPageGeneration(unittest.TestCase):
    def test_extract_title(self):
        heading = extract_title("# Tolkien Fan Club   ")
        self.assertEqual(
            heading, "Tolkien Fan Club",
        )

    def test_extract_title_error(self):
        with self.assertRaises(Exception): 
            extract_title("Tolkien Fan Club")

    # boot.dev tests        
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


if __name__ == "__main__":
    unittest.main()



