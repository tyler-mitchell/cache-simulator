import os
import sys
import math
import argparse

#==============================
#FUNCTIONS
#==============================
def calculate_address_space(address, tag_bits, index_bits, block_offset_bits):
    #convert hex string to binary string
    address_binary = bin(int(address, 16))[2:].zfill(32)
    #get the block offset, tag and index in binary
    block_offset_bin = address_binary[(32 - block_offset_bits):]
    index_bin = address_binary[(32 - block_offset_bits - index_bits):(32 - block_offset_bits)]
    tag_bin = address_binary[:(tag_bits)]
    #print("Tag in binary: " + tag_bin)
    #print("Index in binary: " + index_bin)
    #print("Block Offset in binary: " + block_offset_bin)
    #convert the binary values
    #Block offset as an int
    block_offset = str(int(block_offset_bin, 2))
    #index as an int
    index = str(int(index_bin, 2))
    #tag needs to be hex string
    tag = str(hex(int(tag_bin, 2)))
    #create a list of all the items
    result = [tag, index, block_offset]
    return result

#==============================
#MAIN PROGRAM
#==============================
#Check for proper usage
if len(sys.argv) != 11:
    print ("Usage: " + sys.argv[0] + " –f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    sys.exit(1)
#Block class
class Block:
    def __init__(self, valid, tag ,replace):
        self.tag = tag
        self.valid = valid
        self.replace = replace

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

#==============================
#HEADER AND CACHE CALCULATIONS
#==============================
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
index_size = int(math.log((total_blocks*1024/ args.a), 2))
offset_size = math.log(args.b, 2)
tag_size = int(32 - index_size - offset_size)
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

#==============================
#SIMULATE THE CACHE
#==============================
#First build the 2D array to represent the cache
indices = int(total_indices * 1024) #get the number of rows. Value is in K, convert with 1024
assoc = int(args.a)#block associativity
cache_list = []
block_list = []
#print("Total rows in cache:" + str(indices))
#print("Blocks per row:" + str(assoc))
for row in range(indices):
    #create a list of Block objects
    block_list = []
    for col in range(assoc):
        block_list.append(Block(0,"0",0))
        #print(str(block_list)) #show that the block objects were made correctly
    cache_list.append(block_list)#add this "set" to the index
#print(str(cache_list))#test to see if cache was built correctly

#parse the trace file
f = open(args.f, "r")
if not f:
    print("Error: the file '%s' was not found or could not be opened", args["f"])
    sys.exit(1)

cache_miss_count = 0#cache miss/total lines = cache miss rate. 1 - miss rate = hit rate
total_lines = 0#1 per write to the cache
new_block = True
for line in f:
    if line == '\n':
        new_block = True
        continue
    
    tokens = line.split()

    #Read the first line and retrieve the length and address
    if new_block:
        bytes_read = int(tokens[1][1:3])#element2(length), numbers 2 and 3
        i_address = int(tokens[2], 16)
        hex_address = str(tokens[2])
        #print("Address: 0x%s length=%d byte(s)." % (tokens[2], bytes_read), end=' ')
        new_block = False

        #========================================
        #WRITE TO CACHE / GET CPI / GET MISS RATE
        #========================================
        #get the tag, the index and the block offset
        address_space = calculate_address_space(hex_address, int(tag_size), int(index_size), int(offset_size))#all sizes are in bits
        
        #TODO 
        # insert the adress into the cache
        print("Data inserted into cache block")
        print("Index:" + str(address_space[1]))
        print("Tag:" + str(address_space[0]))
        block = 0#TEST only choose the first block
        cache_miss = False#cache miss on valid == 0 or tag != block tag
        total_lines += 1
        if(cache_list[int(address_space[1])][block].valid == 0):
            cache_list[int(address_space[1])][block].valid = 1#set the valid bit if it's 0
            cache_miss = True#trigger cache miss
            cache_miss_count += 1
            #write to the block(s)
            #TODO write to multiple indexes if needed
            cache_list[int(address_space[1])][block].tag = str(address_space[0])
            print("Valid bit was 0")#TEST remove
        
        #If the valid bit was set and the tags don't match
        if(cache_miss == False) and (cache_list[int(address_space[1])][block].tag != str(address_space[0])):
            cache_miss = True#trigger cache miss
            cache_miss_count += 1
            #Write to the block(s) the new tag
            #TODO write to multiple indexes if needed
            cache_list[int(address_space[1])][block].tag = str(address_space[0])
            print("Tag's don't match")#TEST remove
            

    #Read the second line
    else:
        w_address = hex(int(tokens[1], 16))
        r_address = hex(int(tokens[4], 16))
        
        w_msg =  "Data write at %s, length=4 bytes" % (w_address) if int(w_address, 16) else "No data writes."
        r_msg =  "Data read at %s, length = 4 bytes" % (r_address) if int(r_address, 16) else "No data reads."
        rw_msg = "%s %s" %( w_msg , r_msg)
        #TODO
        #Check if the data in the src/dst is 0.
        #If it is, ignore it. 
        #Otherwise increase the CPI count for this instruction by 2 for a read and 2 for a write
        #print(rw_msg)


#print(str(cache_list))
#print("Rows " + str(indices))
#print("Blocks per row " + str(assoc))

count = 0
for row in cache_list:
    for column in row:
        print("Row #" + str(count) + ", valid bit:" + str(column.valid) + ", tag:" + str(column.tag) + ", replace value:" + str(column.replace))
    count = count + 1 #Keep track of the row, 0 indexed

print("Cache misses:" + str(cache_miss_count))
print("Lines read:" + str(total_lines))
miss_rate = (1 - float(cache_miss_count/total_lines)) * 100
#Print the results
#parser program
print("----- Results -----")
print("Cache Hit Rate: " + "{:.2f}".format(miss_rate) +"%")#TODO: Add cache hit rate result
print("CPI: ")#TODO: Add cache CPI result 
#Milestone 1 requirement: Print the first 20 lines of addresses and lengths
#for i in range(20):
#    print("0x" + str(addresses_list[i]) + ": (" + str(lengths_list[i]) + ")")
