import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.dictionary import DictionaryLoader

class TestDictionaryLoader(unittest.TestCase):
    def test_internal_load(self):
        loader = DictionaryLoader(use_internal=True)
        words = list(loader.load_words())
        self.assertIn("password", words)
        self.assertIn("admin", words)
        
    def test_smart_numeric_mode(self):
        # Test "icrackyou -n" behavior (Smart List)
        loader = DictionaryLoader()
        loader.set_numeric_mode(True)
        # Should generate pins and years
        words = list(loader.load_words())
        self.assertIn("123456", words)
        self.assertIn("2025", words)
        self.assertIn("0000", words) # From short pins loop
        
    def test_brute_force_numeric(self):
        # Test "icrackyou -n -min 2 -max 2" behavior
        loader = DictionaryLoader()
        loader.set_numeric_mode(True)
        loader.set_config(min_len=2, max_len=2)
        words = list(loader.load_words())
        self.assertEqual(len(words), 100) # 00 to 99
        self.assertIn("00", words)
        self.assertIn("99", words)

    def test_brute_force_letters(self):
        # Test "icrackyou -l -min 1 -max 1" behavior
        loader = DictionaryLoader()
        loader.set_numeric_mode(True)
        loader.set_config(min_len=1, max_len=1, charset="abc")
        words = list(loader.load_words())
        self.assertEqual(len(words), 3)
        self.assertIn("a", words)
        self.assertIn("b", words)
        self.assertIn("c", words)

if __name__ == '__main__':
    unittest.main()
