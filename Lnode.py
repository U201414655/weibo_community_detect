class Lnode():
    def __init__(self, l):
        temp = l.split("\t", 5)
        self.id = int(temp[0])
        self.birth = temp[1]
        self.gender = temp[2]
        self.tweet_number = int(temp[3])
        self.tags = temp[4].split(";")
        self.key_word = temp[5].split(";")
        self.group = [int(temp[0])]
