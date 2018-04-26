class Node():
    def __init__(self, s):
        temp = s.split("\t", 5)
        self.name = temp[0]
        self.birth = temp[1]
        self.gender = temp[2]
        self.tweet_number = int(temp[3])
        self.tags = temp[4].split(";")
        self.key_word = temp[5].split(";")
