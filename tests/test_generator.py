import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.generator import PatternGenerator

class TestPatternGenerator(unittest.TestCase):
    def test_numeric_pattern(self):
        gen = PatternGenerator("%%")
        results = list(gen.generate())
        self.assertEqual(len(results), 100) # 00-99
        self.assertIn("00", results)
        self.assertIn("99", results)

    def test_mixed_pattern(self):
        gen = PatternGenerator("a%")
        results = list(gen.generate())
        self.assertEqual(len(results), 10) # a0-a9
        self.assertIn("a0", results)
        self.assertIn("a9", results)

    def test_alpha_pattern(self):
        gen = PatternGenerator("@@")
        results = list(gen.generate())
        self.assertEqual(len(results), 26*26) # aa-zz
        self.assertIn("aa", results)
        self.assertIn("zz", results)

    def test_literal_pattern(self):
        gen = PatternGenerator("test")
        results = list(gen.generate())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "test")

if __name__ == '__main__':
    unittest.main()
