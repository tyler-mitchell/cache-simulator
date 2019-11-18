from row import Row
from block import Block

import random

class Cache:
    index_list = []
    cache_miss_count = 0
    hit_rate = 0
    total_cycles = 0
    total_instructions = 0

    def __init__(self, trace_file, block_size, tag_size, associativity, index_size, offset_size, total_indices, replacement_policy):
        self.block_size = block_size
        self.associativity = associativity
        self.trace_file = trace_file
        self.indices = int(total_indices * 1024)
        self.index_size = index_size
        self.tag_size = tag_size
        self.offset_size = offset_size
        self.replacement_policy = replacement_policy

    # Build the 2D array to represent the cache
    # Get the number of rows. Value is in K, convert with 1024

    def build_cache(self):
        #Each index has a "set" of blocks
        for index in range(self.indices):
            #This row has a list of blocks that represents the "set" in each index of the cache
            self.index_list.append(Row(blocks=[], lastUsedIndex=-1))
            #print("Row #" + str(index))
            for block in range(self.associativity):
                self.index_list[index].blocks.append(Block(valid=0, tag="0", timeSinceLastUse=0)) #add a block to this row
            #print("==" + str(len(self.index_list[index].blocks))) #show that the block objects were made correctly

    def calculate_address_space(self, address, tag_bits, index_bits, block_offset_bits):
        # convert hex string to binary string
        address_binary = bin(int(address, 16))[2:].zfill(32)
        # get the block offset, tag and index in binary
        block_offset_bin = address_binary[(32 - block_offset_bits):]
        index_bin = address_binary[(
            32 - block_offset_bits - index_bits):(32 - block_offset_bits)]
        tag_bin = address_binary[:(tag_bits)]

        # Block offset as an int
        block_offset = int(block_offset_bin, 2)
        # index as an int
        index = int(index_bin, 2)
        # tag needs to be hex string
        tag = int(tag_bin, 2)
        # create a list of all the items

        result = {'tag': tag, 'index': index, 'block_offset': block_offset}
        return result

    def calculate_miss_rate(self):
        # cache miss/total lines = cache miss rate.
        miss_rate = float(self.cache_miss_count/self.total_cycles)
        # 1 - miss rate = hit rate
        self.hit_rate = (1 - miss_rate) * 100

    def get_cache_block(self, address_space):
        # get row by index, get block by tag
        for block in self.index_list[address_space['index']].blocks:
            if block.tag == address_space['tag']:
                return block
        return None
    
    def get_replacement_block(self, address_space):
        row = self.index_list[address_space['index']]
        block = None
        if (self.replacement_policy == "RR"):
            if (row.lastUsedIndex == -1 or row.lastUsedIndex + 1 == self.associativity):
                block = row.blocks[0]
                row.lastUsedIndex = 0
            else:
                block = row.blocks[row.lastUsedIndex + 1]
                row.lastUsedIndex += 1
        elif (self.replacement_policy == "RND"):
            block = row.blocks[random.randint(0, self.associativity)]
        elif (self.replacement_policy == "LRU"):
            block = getLRUBlock(row)
            addOneTimeToAll(row)
            block.timeSinceLastUse = 0
        return block

    def getLRUBlock(self, tag_set):
        numLRU = 0
        blockLRU = tag_set.blocks[0]
        for col in range(self.associativity):
            if (tag_set.blocks[col].timeSinceLastUse > numLRU):
                numLRU = tag_set.blocks[col].timeSinceLastUse
                blockLRU = tag_set.blocks[col]
        return blockLRU

    def addOneTimeToAll(self, tag_set):
        for col in range(self.associativity):
            tag_set.blocks[col].timeSinceLastUse += 1

    def simulate_cache(self):
        tag_size = self.tag_size
        index_size = self.index_size
        trace_file = self.trace_file
        index_list = self.index_list        
        
        self.build_cache()
    
        new_block = True
        for line in trace_file:
            if line == '\n':
                new_block = True
                continue
            tokens = line.split()

            # Read the first line and retrieve the length and address
            if new_block:
                bytes_read = int(tokens[1][1:3])
                i_address = int(tokens[2], 16)
                hex_address = str(tokens[2])
                new_block = False

                # ========================================
                # WRITE TO CACHE / GET CPI / GET MISS RATE
                # ========================================
                # get the tag, the index and the block offset
                address_space = self.calculate_address_space(hex_address, int(tag_size), int(
                    index_size), int(self.offset_size))  # all sizes are in bits

                # TODO
                # insert the adress into the cache
                print("Data inserted into cache block")
                print("Index:" + str(address_space['index']))
                print("Tag:" + str(address_space['tag']))
                
                cache_block = self.get_cache_block(address_space)
                
                # check for cache hit
                # if the valid bit wasn't set or the tags don't match
                if(cache_block == None or cache_block.valid == 0 or cache_block.tag != address_space['tag']): # cache miss
                    cache_block = self.get_replacement_block(address_space)
                    self.cache_miss_count += 1
                    if cache_block.tag != address_space['tag']:
                        print("Tag's don't match") # TEST remove
                    if cache_block.valid == 0:
                        print("Valid bit was 0") # TEST remove
                    # Write to the block(s)
                    # TODO write to multiple indexes if needed
                    cache_block.tag = address_space['tag']
                    # set the valid bit
                    cache_block.valid = 1
                    number_of_reads = self.block_size/4 # block size in bytes divided by 4-byte reads
                    self.total_cycles += 3 * number_of_reads
                else: # cache hit
                    self.total_cycles += 1


            # Read the second line
            else:
                w_address = hex(int(tokens[1], 16))
                r_address = hex(int(tokens[4], 16))
                w_msg = "Data write at %s, length=4 bytes" % (
                    w_address) if int(w_address, 16) else "No data writes."
                r_msg = "Data read at %s, length = 4 bytes" % (
                    r_address) if int(r_address, 16) else "No data reads."
                rw_msg = "%s %s" % (w_msg, r_msg)
                # TODO
                # Check if the data in the src/dst is 0.
                # If it is, ignore it.
                # Otherwise increase the CPI count for this instruction by 2 for a read and 2 for a write
                # print(rw_msg)
                if (w_address is not 0) or (r_address is not 0):
                    self.total_cycles += 2

            self.total_cycles += 2
            self.total_instructions += 1

        self.calculate_miss_rate()

    def display_cache(self):
        # for count, row in enumerate(self.index_list):
        #     for column in row:
        #         print("Row #" + str(count) + ", valid bit:" + str(column.valid) +
        #               ", tag:" + str(column.tag) + ", time since last use value:" + str(column.timeSinceLastUse))

        print("Cache misses:" + str(self.cache_miss_count))
        print("Lines read:" + str(self.total_cycles))
        print("----- Results -----")
        # TODO: Add cache hit rate result
        print("Cache Hit Rate: " + "{:.2f}".format(self.hit_rate) + "%")
        print("CPI: " + str(self.total_cycles/self.total_instructions))
