import re


class Lnode():
    def __init__(self, line):
        line = line.rstrip('\n')
        n = line.split("\t", 5)
        self.id = int(n[0])
        self.is_merged = False
        self.age = self.init_age(n[1])
        self.gender = int(n[2])
        self.tweet_number = int(n[3])
        self.tags = set(n[4].split(";"))
        self.key_words = self.init_key_word(n[5].split(";"))
        self.group = [int(n[0])]

    def init_age(self, birth):
        if re.search("-", birth):
            return 0
        else:
            return 2018 - int(birth)

    def init_key_word(self, key_word_list):
        key_word_ = set()
        for key_word in key_word_list:
            k = key_word.split(":")
            key_word_.add(k[0])
        return key_word_

    @staticmethod
    def are_nodes_similar(lnode1, lnode2):
        weight = 0

        # is age of two nodes similar
        if lnode1.age == 0 or not lnode2.age == 0:
            weight += 0.1
        else:
            age_diff = int(lnode1.age) - (lnode2.age)
            if -3 < age_diff < 3:
                weight += 0.2
            elif -5 < age_diff < 5:
                weight += 0.15
            elif -7 < age_diff < 7:
                weight += 0.1
            elif -10 < age_diff < 10:
                weight += 0.05

        # is gender of two nodes similar
        if lnode1.gender == 0 or lnode2.gender == 0:
            weight += 0.1
        elif -0.1 < lnode1.gender - lnode2.gender < 0.1:
            weight += 0.2
        elif -0.2 < lnode1.gender - lnode2.gender < 0.2:
            weight += 0.15
        elif -0.3 < lnode1.gender - lnode2.gender < 0.3:
            weight += 0.1
        elif -0.4 < lnode1.gender - lnode2.gender < 0.4:
            weight += 0.05

        # is tweet_number od two nodes similar
        if lnode1.tweet_number != 0 and lnode2.tweet_number != 0:
            tweet_number1, tweet_number2 = lnode1.tweet_number, lnode2.tweet_number
            if tweet_number1 < tweet_number2:
                tweet_number1, tweet_number2 = tweet_number2, tweet_number1
            times = tweet_number1 / tweet_number2
            if times < 1.2:
                weight += 0.1
            elif times < 2:
                weight += 0.05

        # is tag of two nodes similar
        min_set_len = len(lnode1.tags) if len(lnode1.tags) <= len(lnode2.tags) else len(lnode2.tags)
        inter_set_len = len(lnode1.tags & lnode2.tags)
        weight += (inter_set_len / min_set_len) * 0.3

        # are key words of two nodes similar
        min_set_len = len(lnode1.key_words) if len(lnode1.key_words) <= len(lnode2.key_words) else len(lnode2.key_words)
        inter_set_len = len(lnode1.key_words & lnode2.key_words)
        weight += (inter_set_len / min_set_len) * 0.2

        return weight

    @staticmethod
    def merge_nodes(lnode1, lnode2):
        len1 = len(lnode1.group)
        len2 = len(lnode2.group)
        if len1 + len2 == 0:
            return
        lnode1.age = (lnode1.age * len1 + lnode2.age * len2) / (len1 + len2)
        lnode1.gender = (lnode1.gender * len1 + lnode2.gender * len2) / (len1 + len2)
        lnode1.tweet_number = (lnode1.tweet_number * len1 + lnode2.tweet_number * len2) / (len1 + len2)
        lnode1.tags = lnode1.tags | lnode2.tags
        lnode1.key_words = lnode1.key_words | lnode2.key_words
        lnode1.group.extend(lnode2.group)
        lnode2.group.clear()
        lnode2.is_merged = True
