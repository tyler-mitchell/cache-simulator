import os
import sys
import argparse
#Check for proper usage
if len(sys.argv) != 11:
    print ("Usage: " + sys.argv[0] + " –f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    sys.exit(1)

parser = argparse.ArgumentParser()#setup the parser
#add the expected argument flags
parser.add_argument('-f', help="The trace file to be parsed", required=True)
parser.add_argument('-s', help="The size of the cache in KB", required=True)
parser.add_argument('-b', help="Block size of the cache", required=True)
parser.add_argument('-a', help="Associativity of the cache", required=True)
parser.add_argument('-r', help="Replacement policy", required=True)
#the args should be in a dictionary containing the arguments
args = vars(parser.parse_args())

#TO-DO: Need to check that the flag's and their values are correct


#Print out the input in the required format
print("Trace File: " + args['f'])
print("Cache Size: " + args['s'] + " KB")#TO-DO: make sure the input only has a number, not letters
print("Block Size: " + args['b'] + " bytes")
print("Associativity: " + args['a'])
print("Policy: " + args['r'])

#Using the inputs above, calculate the values for the cache