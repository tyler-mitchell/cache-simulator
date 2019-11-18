class Block:
    def __init__(self, valid, tag, timeSinceLastUse):
        self.tag = tag
        self.valid = valid
        self.timeSinceLastUse = timeSinceLastUse # used for LRU
        #self.next = False
