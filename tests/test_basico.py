import unittest

class TestSanity(unittest.TestCase):
    def test_matematicas_basicas(self):
        """Prueba que 1 + 1 es 2. Si esto falla, el universo colapsa."""
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()