import math
import unittest
from Louvain import Louvain


class LouvainTest(unittest.TestCase):
    def test_weibo(self):
        # pyl = PyLouvain.from_file("data/arxiv.txt")
        weibo = Louvain("data/action.txt", "data/attribute.txt")
        weibo.cluser()


if __name__ == '__main__':
    unittest.main()
