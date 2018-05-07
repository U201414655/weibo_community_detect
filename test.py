import math
import unittest
from Louvain import Louvain


class LouvainTest(unittest.TestCase):
    def test_weibo(self):
        weibo = Louvain("data/action.txt", "data/attribute.txt")
        weibo.cluster()


if __name__ == '__main__':
    unittest.main()
