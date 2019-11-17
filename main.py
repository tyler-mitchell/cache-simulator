import os
import sys
import math
import argparse
import helpers
from block import Block
from cache import Cache
'''
Cache Capacity = (Block Size in Bytes) * (Blocks per Set) * (Number of Sets)
Index Bits = LOG2(Blocks per Set)
Block Offset Bits = LOG2(Block Size in Bytes)
Tag Bits = (Address Bits) - (Index Bits) - (Block Offset Bits)
Sets = Cache Size / (Block Size * Associativity)
'''


def calculate_address_space(address, tag_bits, index_bits, block_offset_bits):
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
    # convert the binary values
    # Block offset as an int
    block_offset = str(int(block_offset_bin, 2))
    # index as an int
    index = str(int(index_bin, 2))
    # tag needs to be hex string
    tag = str(hex(int(tag_bin, 2)))
    # create a list of all the items
    result = [tag, index, block_offset]
    return result


args = helpers.parse_arguments()
helpers.check_arguments(args)
helpers.display_input(args)

cache_size = args.s
block_size = args.b
associativity = args.a
replacement_policy = args.r
file_name = args.f

# Calculate cache values
total_blocks = ((cache_size * 1024) / block_size) / 1024
index_size = int(math.log((total_blocks*1024 / associativity), 2))
offset_size = math.log(block_size, 2)
tag_size = int(32 - index_size - offset_size)
total_indices = (2 ** index_size) / 1024
memory_overhead = ((tag_size + 1) * associativity *
                   total_indices) / 8  # puts it in KB
memory_impl = (memory_overhead * 1024) + (cache_size * 1024)

helpers.display_calculations(
    total_blocks, tag_size, index_size, total_indices, memory_overhead, memory_impl)

# ==============================
# SIMULATE THE CACHE
# ==============================
# First build the 2D array to represent the cache
# get the number of rows. Value is in K, convert with 1024
indices = int(total_indices * 1024)

# block associativity
cache_list = []
block_list = []


for row in range(indices):
    # create a list of Block objects
    block_list = []
    for col in range(associativity):
        block_list.append(Block(0, "0", 0))
        # print(str(block_list)) #show that the block objects were made correctly
    cache_list.append(block_list)  # add this "set" to the index
# print(str(cache_list))#test to see if cache was built correctly

# parse the trace file
trace_file = open(file_name, "r")
if not trace_file:
    print(
        "Error: the file '%s' was not found or could not be opened", args["f"])
    sys.exit(1)

cache_miss_count = 0  # cache miss/total lines = cache miss rate. 1 - miss rate = hit rate
total_lines = 0  # 1 per write to the cache
new_block = True
for line in trace_file:
    if line == '\n':
        new_block = True
        continue

    tokens = line.split()

    # Read the first line and retrieve the length and address
    if new_block:
        bytes_read = int(tokens[1][1:3])  # element2(length), numbers 2 and 3
        i_address = int(tokens[2], 16)
        hex_address = str(tokens[2])
        #print("Address: 0x%s length=%d byte(s)." % (tokens[2], bytes_read), end=' ')
        new_block = False

        # ========================================
        # WRITE TO CACHE / GET CPI / GET MISS RATE
        # ========================================
        # get the tag, the index and the block offset
        address_space = calculate_address_space(hex_address, int(tag_size), int(
            index_size), int(offset_size))  # all sizes are in bits

        # TODO
        # insert the adress into the cache
        print("Data inserted into cache block")
        print("Index:" + str(address_space[1]))
        print("Tag:" + str(address_space[0]))
        block = 0  # TEST only choose the first block
        cache_miss = False  # cache miss on valid == 0 or tag != block tag
        total_lines += 1
        if(cache_list[int(address_space[1])][block].valid == 0):
            # set the valid bit if it's 0
            cache_list[int(address_space[1])][block].valid = 1
            cache_miss = True  # trigger cache miss
            cache_miss_count += 1
            # write to the block(s)
            # TODO write to multiple indexes if needed
            cache_list[int(address_space[1])][block].tag = str(
                address_space[0])
            print("Valid bit was 0")  # TEST remove

        # If the valid bit was set and the tags don't match
        if(cache_miss == False) and (cache_list[int(address_space[1])][block].tag != str(address_space[0])):
            cache_miss = True  # trigger cache miss
            cache_miss_count += 1
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


# print(str(cache_list))
#print("Rows " + str(indices))
#print("Blocks per row " + str(assoc))

count = 0
for row in cache_list:
    for column in row:
        print("Row #" + str(count) + ", valid bit:" + str(column.valid) +
              ", tag:" + str(column.tag) + ", replace value:" + str(column.replace))
    count = count + 1  # Keep track of the row, 0 indexed


print("Cache misses:" + str(cache_miss_count))
print("Lines read:" + str(total_lines))
miss_rate = (1 - float(cache_miss_count/total_lines)) * 100
# Print the results
# parser program
print("----- Results -----")
# TODO: Add cache hit rate result
print("Cache Hit Rate: " + "{:.2f}".format(miss_rate) + "%")
print("CPI: ")  # TODO: Add cache CPI result
# Milestone 1 requirement: Print the first 20 lines of addresses and lengths
# for i in range(20):
#    print("0x" + str(addresses_list[i]) + ": (" + str(lengths_list[i]) + ")")
