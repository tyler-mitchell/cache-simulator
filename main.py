import os
import sys
import math
import argparse
#from parser.py import parseTraceFile
#Check for proper usage
if len(sys.argv) != 11:
    print ("Usage: " + sys.argv[0] + " –f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    sys.exit(1)

cmd_parser = argparse.ArgumentParser()#setup the parser
#add the expected argument flags
cmd_parser.add_argument('-f',type=str, action='store', help="The trace file to be parsed")
cmd_parser.add_argument('-s', type=int, action='store',help="The size of the cache in KB")
cmd_parser.add_argument('-b',type=int, action='store', help="Block size of the cache")
cmd_parser.add_argument('-a', type=int, action='store', help="Associativity of the cache")
cmd_parser.add_argument('-r', type=str, action='store', help="Replacement policy")
#the args should be in a dictionary containing the arguments
args = cmd_parser.parse_args()

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

#Print header
print("Cache Simulator CS 3853 Spring 2019 - Group # 9")
#Print command line
print("Cmd Line: " + str(sys.argv[::1]))
#Print out the input in the required format
print("Trace File: " + args.f)
print("Cache Size: " + str(args.s) + " KB")#TO-DO: make sure the input only has a number, not letters
print("Block Size: " + str(args.b) + " bytes")
print("Associativity: " + str(args.a))
print("R-Policy: " + str(args.r))

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

#Execute the trace file parser
#parser program here and run it on the trace file given

# Example trace file:

#   EIP (07): 7c80976b 8b 84 88 10 0e 00 00 mov eax,[eax+ecx*4+0xe10]
#   dstM: 7ffdf034 00000000    srcM: 7ffdfe2c 901e8b00

# EIP: (Extended Instruction Pointer): identifies the memory that is read containing the instruction.
# 07: the number of bytes read--always a 2 digit number 
# 7c80976b: numeric address containing the instruction.
# 8b 84 88 10 0e 00 00: machine code (data) don't parse data
# dstM: 7ffdf034: data write address--if data being read is all 0s, ignore it (assume 4 bytes)
# 00000000: write data--ignore
# srcM: 7ffdfe2c: data read address--if data being read is all 0s, ignore it (assume 4 bytes)
# 901e8b00: read data--ignore

#Function to parse the trace file
f = open(args.f, "r")
#Milestone 1 requires first 20 addresses and lengths to be printed
addresses_list = [] #hex addresses
lengths_list = [] #lengths of each read
if not f:
    print("Error: the file '%s' was not found or could not be opened", args["f"])
    sys.exit(1)

new_block = True
for line in f:
    if line == '\n':
        new_block = True
        continue
    
    tokens = line.split()
    # TODO:
    #   pad hex with zero(s)
    if new_block:
        bytes_read = int(tokens[1][1:3])#element2(length), numbers 2 and 3
        i_address = int(tokens[2], 16)
        print("Address: 0x%s length=%d byte(s)." % (tokens[2], bytes_read), end=' ')
        new_block = False

        #milestone 1 code
        addresses_list.append(str(tokens[2]))#get the raw hex address
        lengths_list.append(bytes_read)#length of instruction
    else:
        w_address = hex(int(tokens[1], 16))
        r_address = hex(int(tokens[4], 16))
        
        w_msg =  "Data write at %s, length=4 bytes" % (w_address) if int(w_address, 16) else "No data writes."
        r_msg =  "Data read at %s, length = 4 bytes" % (r_address) if int(r_address, 16) else "No data reads."
        rw_msg = "%s %s" %( w_msg , r_msg)
    
        print(rw_msg)

#Print the results of the cmd_
#parser program
print("----- Results -----")
print("Cache Hit Rate: " + "%")#TODO: Add cache hit rate result
print("CPI: ")#TODO: Add cache CPI result 
#Milestone 1 requirement: Print the first 20 lines of addresses and lengths
for i in range(20):
    print("0x" + str(addresses_list[i]) + ": (" + str(lengths_list[i]) + ")")
