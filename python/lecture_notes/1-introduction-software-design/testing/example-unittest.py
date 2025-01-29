import unittest

def multiply(x, y):
    return x * y

class MultiplyTest(unittest.TestCase):

    def test_3_times_4(self):
        self.assertEqual(multiply(3, 4), 12)

if __name__ == '__main__':
    unittest.main()
