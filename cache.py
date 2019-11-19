from block import Block

import random


class Cache:
    index_list = []
    cache_miss_count = 0
    hit_rate = 0
    total_cycles = 0
    total_instructions = 0

    def __init__(self, trace_file, block_size, tag_size, indices, associativity, index_size, offset_size,  replacement_policy):
        self.block_size = block_size
        self.associativity = associativity
        self.trace_file = trace_file
        self.indices = indices
        self.index_size = index_size
        self.tag_size = tag_size
        self.offset_size = offset_size
        self.replacement_policy = replacement_policy

    # Build the 2D array to represent the cache
    # Get the number of rows. Value is in K, convert with 1024
    def build_cache(self):
        # Each index has a "set" of blocks
        for index in range(self.indices):
            # create a list of Block objects
            # This "block_list" represents the "set" in each index of the cache
            block_list = []
            for block in range(self.associativity):
                block_list.append(Block(0, "0", 0))  # add a block to this row
                # show that the block objects were made correctly
                # print("==" + str(block_list))
            self.index_list.append(block_list)  # add this "set" to the index

    def calculate_address_space(self, address, tag_bits, index_bits, block_offset_bits):
        # convert hex string to binary string
        address_binary = bin(int(address, 16))[2:].zfill(32)
        # get the block offset, tag and index in binary
        block_offset_bin = address_binary[(32 - block_offset_bits):]
        index_bin = address_binary[(
            32 - block_offset_bits - index_bits):(32 - block_offset_bits)]
        tag_bin = address_binary[:(tag_bits)]

        # Block offset as an int
        block_offset = str(int(block_offset_bin, 2))
        # index as an int
        index = int(index_bin, 2)
        # tag needs to be hex string
        tag = str(hex(int(tag_bin, 2)))
        # create a list of all the items

        result = {'tag': tag, 'index': index, 'block_offset': block_offset}
        return result

    def calculate_hit_rate(self):
        # cache miss/total lines = cache miss rate.
        miss_rate = float(self.cache_miss_count/self.total_cycles)
        # 1 - miss rate = hit rate
        self.hit_rate = (1 - miss_rate) * 100

    def simulate_cache(self):
        tag_size = self.tag_size
        index_size = self.index_size
        trace_file = self.trace_file
        index_list = self.index_list
        block_size = self.block_size

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

                # get the tag, the index and the block offset
                address_space = self.calculate_address_space(hex_address, int(tag_size), int(
                    index_size), int(self.offset_size))  # all sizes are in bits
                cache_hit = False

                print("Data to be inserted into cache block")
                print("Index:" + str(address_space['index']))
                print("Tag:" + address_space['tag'])

                # HANDLING ROLLOVER INTO OTHER ROWS                # get the number of rows to be read
                offset = address_space['block_offset']  # get the offset
                index_rollover = int(
                    (int(offset) + bytes_read) / block_size)
                if((int(offset) + bytes_read % block_size) != 0):  # if there is a remainder
                    index_rollover += 1  # add a row to be read

                # Sometimes our offset and read size will "rollover" into other rows and their blocks
                for rollover in range(0, index_rollover):
                    # get the correct row to check
                    current_index = rollover + address_space['index']
                    #This handles going beyond the cache index for a rollover
                    if (current_index + 1) >= self.indices:
                        #go to the first index
                        current_index = current_index - self.indices
                    #print("rows in the cache: " + str(self.indices))
                    print("Rollover: " + str(rollover))
                    #print("Base Index: " + str(address_space['index']))
                    #print("current index: " + str(current_index))

                    # Given the tag and index, try to find the block that matches this tag in the set at this index
                    # check this row's blocks for a match
                    for cache_block in index_list[current_index]:
                        if cache_block.tag == address_space['tag']:
                            cache_hit = True  # the block has been found!

                    # NO MATCHING TAG FOUND, BEGIN REPLACEMENT
                    if (cache_hit == False):
                        empty_block = False
                        self.cache_miss_count += 1  # This counts as a miss
                        # find an empty block to replace
                        for cache_block in index_list[address_space['index']]:
                            if (cache_block.valid == 0):
                                # empty block found, fill in the tag
                                #print("Empty block found")
                                cache_block.valid = 1  # the block now has a tag
                                empty_block = True  # No need for replacement algorithm if empty block was found
                                break  # exit the loop and get out of this set

                        # if no empty block was found, engage the replacement algorithm
                        if empty_block == False:
                            print("Executing replacement algorithm")
                            # rr
                            if(self.replacement_policy == "RR"):
                                first_time = True
                                count = 0
                                for cache_block in index_list[current_index]:
                                    if cache_block.next == True:
                                        # replace
                                        cache_block.tag = address_space['tag']
                                        cache_block.next = False
                                        first_time = False
                                        # update next block
                                        # if not the last block, update the next one
                                        if (count + 1) < self.associativity:#check that the next block isn't out of range(remember 0 indexing)
                                            index_list[current_index][(count + 1)].next = True
                                        else:
                                            index_list[current_index][0].next = True
                                    count += 1

                                if(first_time == True):
                                    # set first block to next
                                    index_list[current_index][0].next = True
                            elif(self.replacement_policy == "RND"):
                                # For the Random algorithm just pick a block index at random. Literally get a value and go to
                                # index_list[address_space['index']][RANDOM NUMBER GOES HERE].tag = new tag
                                #Assuming no blocks are empty, which is how we got to this point
                                #get a random number in the range of 0 to our associativity.
                                random_num = random.randrange(0,self.associativity)
                                print("Random number chosen: " + str(random_num))
                                index_list[current_index][random_num].tag = address_space['tag']
                                print("Block " + str(random_num) + " replaced with " + address_space['tag'])

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
                if (w_address != 0) or (r_address != 0):
                    self.total_cycles += 2

            self.total_cycles += 2
            self.total_instructions += 1

        self.calculate_hit_rate()

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
