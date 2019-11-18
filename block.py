class Block:
    def __init__(self, valid, tag, next):
        self.tag = tag
        self.valid = valid
        # self.timeSinceLastUse = timeSinceLastUse # used for LRU
        self.next = next
