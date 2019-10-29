import os
import sys
import math
import argparse
#Check for proper usage
if len(sys.argv) != 11:
    print ("Usage: " + sys.argv[0] + " –f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    sys.exit(1)

parser = argparse.ArgumentParser()#setup the parser
#add the expected argument flags
parser.add_argument('-f',type=str, action='store', help="The trace file to be parsed")
parser.add_argument('-s', type=int, action='store',help="The size of the cache in KB")
parser.add_argument('-b',type=int, action='store', help="Block size of the cache")
parser.add_argument('-a', type=int, action='store', help="Associativity of the cache")
parser.add_argument('-r', type=str, action='store', help="Replacement policy")
#the args should be in a dictionary containing the arguments
args = parser.parse_args()

#Check that the flag's and their values are correct
if (args.s < 1) or (args.s > 8192):#size of cache flag
    print("Cache size out of range: 1Kb - 8192Kb (8MB)")
    sys.exit(1)
if (args.b < 4) or (args.b > 64):#block size flag
    print("Block size out of range: 4 bytes - 64 bytes")
    sys.exit(1)
associativity = [1,2,4,8,16] #these are valid associativity input
if not (args.a in associativity):#associativity flag
    print("Associativity out of range: 1, 2, 4, 8, 16")
    sys.exit(1)
replacements = ["RR", "RND"]
if not (args.r in replacements):
    print("Unkown replacement policy. Must be either RR or RND")
    sys.exit(1)


#Print out the input in the required format
print("Trace File: " + args.f)
print("Cache Size: " + str(args.s) + " KB")#TO-DO: make sure the input only has a number, not letters
print("Block Size: " + str(args.b) + " bytes")
print("Associativity: " + str(args.a))
print("Policy: " + str(args.r))

#Using the inputs above, calculate the values for the cache
total_blocks = ((args.s * 1024)/ args.b) / 1024
index_size = math.log((total_blocks*1024/ args.a), 2)
offset_size = math.log(args.b, 2)
tag_size = 32 - index_size - offset_size
total_indices = (2 ** index_size) / 1024
memory_overhead = ((tag_size + 1) * args.a * total_indices) / 8 #puts it in KB
memory_impl = (memory_overhead * 1024) + (args.s * 1024)
#print out the calculations
print("----- Calculated Values -----")
print("Total #Blocks: " + str(total_blocks) + "KB (2^" + str(math.log(total_blocks,2) + 10) + ")")
print("Tag Size: " + str(tag_size) + " bits")
print("Index size: " + str(index_size) + "bits, Total Indices: " + str(total_indices) + "KB")
print("Overhead Memory Size: " + str(memory_overhead * 1024) + " bytes (or " + str(memory_overhead) + "KB)")
print("Implementation Memory Size: " + str(memory_impl) + " bytes (or " + str(memory_impl/1024) +" KB)")

#Execute the trace file parser program here and run it on the trace file given
traceFile = str(args.f)

#Print the results of the parser program
print("----- Results -----")
print("Cache Hit Rate: " + "%")#TO-DO: Add cache hit rate result
print("CPI: ")#TO-DO: Add cache CPI result