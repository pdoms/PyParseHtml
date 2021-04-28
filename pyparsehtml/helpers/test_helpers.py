import unittest
import helpers_parse_initial as helpers


class TestHelpers_parse_initial(unittest.TestCase):
    def test_mergeDict(self):
        """
        Test that dictionaries get concatetnated to one. 
        """
        data = [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]
        result = helpers.mergeDict(data)
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3, "d": 4})
    
    def test_isSelfCloser(self):
        pass

if __name__ == '__main__':
    unittest.main()