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

# parse arguments
args = helpers.parse_arguments()

# validate arguments
helpers.check_arguments(args)

# initialize variables
cache_size = args.s
block_size = args.b
associativity = args.a

replacement_policy = args.r
file_name = args.f

# open trace file
trace_file = helpers.get_trace_file(file_name)

# display input
helpers.display_input(args)


# calculate cache values
total_blocks = (((cache_size * 1024) / block_size) / 1024)
index_size = int(math.log((total_blocks*1024 // associativity), 2))
offset_size = math.log(block_size, 2)
tag_size = int(32 - index_size - offset_size)
total_indices = (2 ** index_size) / 1024
indices = int(total_indices * 1024)
memory_overhead = ((tag_size + 1) * associativity *
                   total_indices) / 8  # puts it in KB
memory_impl = (memory_overhead * 1024) + (cache_size * 1024)

# display calculations
helpers.display_calculations(
    total_blocks, tag_size, index_size, total_indices, memory_overhead, memory_impl)


# simulate the cache
cache = Cache(trace_file=trace_file, indices=indices, block_size=block_size, tag_size=tag_size, associativity=associativity,
              index_size=index_size, offset_size=offset_size, replacement_policy=replacement_policy)
cache.simulate_cache()
cache.display_cache()


# Milestone 1 requirement: Print the first 20 lines of addresses and lengths
# for i in range(20):
#    print("0x" + str(addresses_list[i]) + ": (" + str(lengths_list[i]) + ")")
