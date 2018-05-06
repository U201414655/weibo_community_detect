class Node():
    def __init__(self, s, no):
        temp = s.split("\t", 5)
        self.no = no
        self.id = temp[0]
        self.birth = temp[1]
        self.gender = temp[2]
        self.tweet_number = int(temp[3])
        self.tags = temp[4].split(";")
        self.key_word = temp[5].split(";")
        self.group = [temp[0]]
