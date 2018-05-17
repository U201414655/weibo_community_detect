import sys
import math
import unittest
from Louvain import Louvain


class LouvainTest(unittest.TestCase):
    def test_weibo(self):
        result_file = open("data/result.txt", "w", encoding="UTF-8")
        sys.stdout = result_file
        weibo = Louvain("data/action.txt", "data/attribute.txt")
        best_q, partition = weibo.community_detect()
        print ("Tne number of communities:\t", len(partition))
        print ("best_q:\t", best_q)
        for p in partition:
            print (p)
        result_file.close()


if __name__ == '__main__':
    unittest.main()
