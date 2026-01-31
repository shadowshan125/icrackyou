import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.filters import FilterEngine

class TestFilterEngine(unittest.TestCase):
    def test_length_filters(self):
        config = {'min_length': 4, 'max_length': 6}
        engine = FilterEngine(config)
        words = ["hi", "pass", "longer", "toolongword"]
        results = list(engine.filter(words))
        self.assertIn("pass", results)
        self.assertIn("longer", results)
        self.assertNotIn("hi", results)
        self.assertNotIn("toolongword", results)

    def test_content_policies(self):
        config = {'require_numbers': True}
        engine = FilterEngine(config)
        words = ["pass", "pass1", "123", "no_num"]
        results = list(engine.filter(words))
        self.assertNotIn("pass", results)
        self.assertIn("pass1", results)
        self.assertIn("123", results)
        self.assertNotIn("no_num", results)
        
    def test_limit(self):
        config = {'limit': 2}
        engine = FilterEngine(config)
        words = ["one", "two", "three", "four"]
        results = list(engine.filter(words))
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ["one", "two"])

if __name__ == '__main__':
    unittest.main()
