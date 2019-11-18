import argparse
import sys
import math


def parse_arguments():
    # Check for proper usage
    if len(sys.argv) != 11:
        print(
            "Usage: " + sys.argv[0] + " –f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
        sys.exit(1)

    cmd_parser = argparse.ArgumentParser()  # setup the parser
    # add the expected argument flags
    cmd_parser.add_argument('-f', type=str, action='store',
                            help="The trace file to be parsed")
    cmd_parser.add_argument('-s', type=int, action='store',
                            help="The size of the cache in KB")
    cmd_parser.add_argument('-b', type=int, action='store',
                            help="Block size of the cache")
    cmd_parser.add_argument('-a', type=int, action='store',
                            help="Associativity of the cache")
    cmd_parser.add_argument(
        '-r', type=str, action='store', help="Replacement policy")
    # the args should be in a dictionary containing the arguments
    args = cmd_parser.parse_args()
    return args


def check_arguments(args):
    # Check that the flag's and their values are correct
    if (args.s < 1) or (args.s > 8192):  # size of cache flag
        print("Cache size out of range: 1Kb - 8192Kb (8MB)")
        sys.exit(1)
    if (args.b < 4) or (args.b > 64):  # block size flag
        print("Block size out of range: 4 bytes - 64 bytes")
        sys.exit(1)
    associativity = [1, 2, 4, 8, 16]  # these are valid associativity input
    if not (args.a in associativity):  # associativity flag
        print("Associativity out of range: 1, 2, 4, 8, 16")
        sys.exit(1)
    replacements = ["RR", "RND"]
    if not (args.r in replacements):
        print("Unkown replacement policy. Must be either RR or RND")
        sys.exit(1)


def display_input(args):
    # Print header
    print("Cache Simulator CS 3853 Spring 2019 - Group # 9")
    # Print command line
    print("Cmd Line: " + str(sys.argv[::1]))
    # Print out the input in the required format
    print("Trace File: " + args.f)
    # TO-DO: make sure the input only has a number, not letters
    print("Cache Size: " + str(args.s) + " KB")
    print("Block Size: " + str(args.b) + " bytes")
    print("Associativity: " + str(args.a))
    print("R-Policy: " + str(args.r))


def display_calculations(total_blocks, tag_size, index_size, total_indices, memory_overhead, memory_impl):
    # print out the calculations
    print("----- Calculated Values -----")
    print(
        f"Total # Blocks: {total_blocks}KB (2^{int(math.log(total_blocks, 2) + 10)})")
    print(f"Tag Size: {tag_size} bits")
    print(f"Index size: {index_size} bits, Total Indices: {total_indices} KB")
    print(
        f"Overhead Memory Size: {memory_overhead * 1024} bytes (or {memory_overhead} KB)")
    print(
        f"Implementation Memory Size: {memory_impl} bytes (or {memory_impl/1024} KB )")


def get_trace_file(file_name):
    trace_file = open(file_name, "r")
    if not trace_file:
        print(
            "Error: the file '%s' was not found or could not be opened", file_name)
        sys.exit(1)
    return trace_file
