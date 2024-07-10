from rest_framework.test import APITestCase


class CustomAPITestCase(APITestCase):
    def assertDictIncludes(self, actual, expected):
        """
        Custom assertion function to compare dictionaries, including only keys present in `expected`.
        """
        self.assertIsInstance(actual, dict, "First argument is not a dictionary")
        self.assertIsInstance(expected, dict, "Second argument is not a dictionary")

        filtered_actual = {key: actual[key] for key in expected.keys()}
        if not expected == filtered_actual:
            self.fail(f"Expected {expected}, but got {actual}")
