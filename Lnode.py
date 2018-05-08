class Lnode():
    def __init__(self, line):
        line = line.rstrip('\n')
        n = line.split("\t", 5)
        self.id = int(n[0])
        self.is_combined = False
        self.birth = n[1]
        self.gender = n[2]
        self.tweet_number = int(n[3])
        self.tags = n[4].split(";")
        self.key_word = n[5].split(";")
        self.group = [int(n[0])]
