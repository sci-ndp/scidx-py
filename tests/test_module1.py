import unittest
from scidx import module1

class TestModule1(unittest.TestCase):
    def test_function(self):
        self.assertEqual(module1.function(), "Hello, world!")

if __name__ == '__main__':
    unittest.main()
