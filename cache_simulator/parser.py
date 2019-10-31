import os
import sys
import math
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
def parseTraceFile( traceFile ):

    return 0



