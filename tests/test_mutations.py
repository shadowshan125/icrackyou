import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.mutations import MutationEngine

class TestMutationEngine(unittest.TestCase):
    def test_case_transformations(self):
        config = {'upper': True, 'lower': True}
        engine = MutationEngine(config)
        words = ["Test"]
        results = list(engine.process(words))
        self.assertIn("TEST", results)
        self.assertIn("test", results)
    
    def test_smart_numbers(self):
        config = {'numbers': True}
        engine = MutationEngine(config)
        words = ["pass"]
        results = list(engine.process(words))
        # Smart numbers logic is dynamic (years), but '1' and '123' are static
        self.assertIn("pass123", results)
        self.assertIn("pass1", results)

    def test_prefix_suffix(self):
        config = {'prefix': ['pre_'], 'suffix': ['_suf']}
        engine = MutationEngine(config)
        words = ["word"]
        results = list(engine.process(words))
        # Expect: word, word_suf, pre_word, pre_word_suf
        self.assertIn("word", results)
        self.assertIn("word_suf", results)
        self.assertIn("pre_word", results)
        self.assertIn("pre_word_suf", results)

    def test_reverse(self):
        config = {'reverse': True}
        engine = MutationEngine(config)
        words = ["admin"]
        results = list(engine.process(words))
        self.assertIn("nimda", results)
        self.assertIn("admin", results)

    def test_repeat(self):
        config = {'repeat': True}
        engine = MutationEngine(config)
        words = ["admin"]
        results = list(engine.process(words))
        self.assertIn("adminadmin", results)

    def test_sandwich(self):
        # Sandwich uses prefix/suffix internal lists.
        # Use implicit smart numbers to trigger suffix list, or custom.
        config = {'sandwich': True, 'suffix': ['123']}
        engine = MutationEngine(config)
        words = ["admin"]
        results = list(engine.process(words))
        self.assertIn("123admin123", results)

if __name__ == '__main__':
    unittest.main()
