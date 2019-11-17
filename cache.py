from block import Block


class Cache:
    cache_list = []
    block_list = []
    cache_miss_count = 0
    miss_rate = 0
    total_lines = 0

    def __init__(self, trace_file, block_size, tag_size, associativity, index_size, offset_size, total_indices):
        self.block_size = block_size
        self.associativity = associativity
        self.trace_file = trace_file
        self.indices = int(total_indices * 1024)
        self.index_size = index_size
        self.tag_size = tag_size
        self.offset_size = offset_size
        


    # Build the 2D array to represent the cache
    # Get the number of rows. Value is in K, convert with 1024
    def build_cache(self):
        for row in range(self.indices):
            # create a list of Block objects
            block_list = []
            for col in range(self.associativity):
                block_list.append(Block(0, "0", 0))
                # print(str(block_list)) #show that the block objects were made correctly
            self.cache_list.append(block_list)  # add this "set" to the index

        # print(str(cache_list))#test to see if cache was built correctly

    def calculate_address_space(self, address, tag_bits, index_bits, block_offset_bits):
        # convert hex string to binary string
        address_binary = bin(int(address, 16))[2:].zfill(32)
        # get the block offset, tag and index in binary
        block_offset_bin = address_binary[(32 - block_offset_bits):]
        index_bin = address_binary[(
            32 - block_offset_bits - index_bits):(32 - block_offset_bits)]
        tag_bin = address_binary[:(tag_bits)]
        #print("Tag in binary: " + tag_bin)
        #print("Index in binary: " + index_bin)
        #print("Block Offset in binary: " + block_offset_bin)

        # Block offset as an int
        block_offset = str(int(block_offset_bin, 2))
        # index as an int
        index = str(int(index_bin, 2))
        # tag needs to be hex string
        tag = str(hex(int(tag_bin, 2)))
        # create a list of all the items
        result = [tag, index, block_offset]
        return result

    def calculate_miss_rate(self):
        # cache miss/total lines = cache miss rate. 1 - miss rate = hit rate
        self.miss_rate = (
            1 - float(self.cache_miss_count/self.total_lines)) * 100

 
    def simulate_cache(self):
        self.build_cache()
        # 1 per write to the cache
        new_block = True
        for line in self.trace_file:
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
                address_space = self.calculate_address_space(hex_address, int(self.tag_size), int(
                    self.index_size), int(self.offset_size))  # all sizes are in bits

                # TODO
                # insert the adress into the cache
                print("Data inserted into cache block")
                print("Index:" + str(address_space[1]))
                print("Tag:" + str(address_space[0]))
                block = 0  # TEST only choose the first block
                cache_miss = False  # cache miss on valid == 0 or tag != block tag
                self.total_lines += 1
                if(self.cache_list[int(address_space[1])][block].valid == 0):
                    # set the valid bit if it's 0
                    self.cache_list[int(address_space[1])][block].valid = 1
                    cache_miss = True  # trigger cache miss
                    self.cache_miss_count += 1
                    # write to the block(s)
                    # TODO write to multiple indexes if needed
                    self.cache_list[int(address_space[1])][block].tag = str(
                        address_space[0])
                    print("Valid bit was 0")  # TEST remove

                # If the valid bit was set and the tags don't match
                if(cache_miss == False) and (self.cache_list[int(address_space[1])][block].tag != str(address_space[0])):
                    cache_miss = True  # trigger cache miss
                    self.cache_miss_count += 1
                    # Write to the block(s) the new tag
                    # TODO write to multiple indexes if needed
                    cache_list[int(address_space[1])][block].tag = str(
                        address_space[0])
                    print("Tag's don't match")  # TEST remove

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

        self.calculate_miss_rate()

    def display_cache(self):
        for count, row in enumerate(self.cache_list):
            for column in row:
                print("Row #" + str(count) + ", valid bit:" + str(column.valid) +
                      ", tag:" + str(column.tag) + ", replace value:" + str(column.replace))

        print("Cache misses:" + str(self.cache_miss_count))
        print("Lines read:" + str(self.total_lines))
        print("----- Results -----")
        # TODO: Add cache hit rate result
        print("Cache Hit Rate: " + "{:.2f}".format(self.miss_rate) + "%")
        print("CPI: ")  # TODO: Add cache CPI result
