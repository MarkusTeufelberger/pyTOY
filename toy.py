# Rechnerorganisation TU Graz 2012
# Implementation of "TOY" (see http://introcs.cs.princeton.edu/xtoy/) in Python
# Inspired by "spielzeug_computer_1.c" by Prof. KC Posch
# Written by Markus Teufelberger (markus.teufelberger@student.tugraz.at)
# All rights reserved, for educational use only, use at your own risk,
# no warranties, this program might kill your hamster or worse!

import sys
import string

#helper function for input filtering
def ishex(s):
  for c in s:
    if not c in string.hexdigits: return False
  return True

def initialize_memory(memory, register):
  """Load the program into memory.
  
  Currently fixed values, in the future values should be loaded from a file.
  """

  memory[0x00] = 0x0007
  memory[0x01] = 0x000C
  
  memory[0x10] = 0x8100 #ld R1, 0
  memory[0x11] = 0x8201 #ld R2, 1
  memory[0x12] = 0x1312 #add R3, R1, R2
  memory[0x13] = 0x9302 #st R3, 2
  memory[0x14] = 0x84FF #ld R4, FF (stdin)
  memory[0x15] = 0x9403 #st R4, 3
  memory[0x16] = 0x0000 #hlt

def load_stdin(memory):
  data = raw_input("Please enter up to 4 digits in hexadecimal format: 0x")
  data = filter(ishex, data)
  number = int("0x" + data, 16)
  number &= 0xFFFF #mask numbers higher than 0xFFFF, only 4 digit inputs
  print "Input from stdin: {:04X}".format(number)
  memory[0xFF] = number

def store_stdout(memory, register, d)
  print "Output to stdout: {:04X}".format(register[d])

#the 16 commands toy understands:
#0 halt

#1 add
def func_add(op,d,s,t,memory,register):
  register[d] = register[s] + register[t]

#2 subtract
def func_subtract(op,d,s,t,memory,register):
  register[d] = register[s] - register[t]

#3 and
def func_and(op,d,s,t,memory,register):
  register[d] = register[s] & register[t]

#4 xor
def func_xor(op,d,s,t,memory,register):
  register[d] = register[s] ^ register[t]

#5 shift left
def func_shift_left(op,d,s,t,memory,register):
  register[d] = register[s] << register[t]

#6 shift right
def func_shift_right(op,d,s,t,memory,register):
  register[d] = register[s] >> register[t]

#7 load immediate
def func_load_immediate(op,d,s,t,memory,register):
  register[d] = s*16 + t

#8 load
def func_load(op,d,s,t,memory,register):
  #loading from memory[0xFF] loads from stdin
  if s*16 + t == 0xFF:
    load_stdin(memory)
  register[d] = memory[s*16 + t]

#9 store
def func_store(op,d,s,t,memory,register):
  #stores to FF go to stdout
  if s*16 + t == 0xFF:
    store_stdout(memory, register, d)
  memory[s*16 + t] = register[d]

#A load indirect
def func_load_indirect(op,d,s,t,memory,register):
  #loading from memory[0xFF] loads from stdin
  if register[t] == 0xFF:
    load_stdin(memory)
  register[d] = memory[register[t]]

#B store indirect
def func_store_indirect(op,d,s,t,memory,register):
  if register[t] == 0xFF:
    store_stdout(memory, register, d)
  memory[register[t]] = register[d]

#C branch zero
def func_branch_zero(op,d,s,t,memory,register, PC):
  if register[d] == 0:
    PC = s*16 + t

#D branch positive
def func_branch_positive(op,d,s,t,memory,register, PC):
  if register[d] > 0:
    PC = s*16 + t

#E jump register
def func_jump_register(op,d,s,t,memory,register, PC):
  PC = register[d]

#F jmp and link
def func_jump_and_link(op,d,s,t,memory,register, PC):
  register[d] = PC
  PC = s*16 + t

def show_memory(memory):
  """Display the 256 memory addresses as hex values"""
  print "----------TOY memory-----------"
  for i in range(0,32):
    for j in range(0,8):
      try:
        print "{:02X}:{:04X}".format(32*j+i, memory[32*j+i]),
      except KeyError:
        print "{:02X}:????".format(32*j+i),
    print "\n", #fyi: , at the end of a "print" line means no automatic EOL

def main(argv=None):
  if argv is None:
    argv = sys.argv
  memory = {} #256 memory addresses, not enforced
  register = {} #16 registers, also not enforced

  PC = 0x10 #Program counter
  IR = None #Instruction register

  #alias names for bitfields in IR
  op = None
  d = None
  s = None
  t = None

  #initialize
  initialize_memory(memory, register)
  print "Initial memory configuration:"
  show_memory(memory)
  while(1):
    #Fetch
    IR = memory[PC]
    PC += 1
    op = (IR >> 12) & 0xF
    d = (IR >> 8) & 0xF
    s = (IR >> 4) & 0xF
    t = (IR >> 0) & 0xF
    print "IR:{:02X}, PC:{:02X}, op:{:01X}, d:{:01X}, s:{:01X}, t:{:01X}".format(IR, PC, op, d, s, t)
    #Execute

    #register[0] is always 0!
    register[0] = 0

    if op == 0x0:
      break
    elif op == 0x1:
      func_add(op,d,s,t,memory,register)
    elif op == 0x2:
      func_subtract(op,d,s,t,memory,register)
    elif op == 0x3:
      func_and(op,d,s,t,memory,register)
    elif op == 0x4:
      func_xor(op,d,s,t,memory,register)
    elif op == 0x5:
      func_shift_left(op,d,s,t,memory,register)
    elif op == 0x6:
      func_shift_right(op,d,s,t,memory,register)
    elif op == 0x7:
      func_load_immediate(op,d,s,t,memory,register)
    elif op == 0x8:
      func_load(op,d,s,t,memory,register)
    elif op == 0x9:
      func_store(op,d,s,t,memory,register)
    elif op == 0xA:
      func_load_indirect(op,d,s,t,memory,register)
    elif op == 0xB:
      func_store_indirect(op,d,s,t,memory,register)
    elif op == 0xC:
      func_branch_zero(op,d,s,t,memory,register, PC)
    elif op == 0xD:
      func_branch_positive(op,d,s,t,memory,register, PC)
    elif op == 0xE:
      func_jump_register(op,d,s,t,memory,register, PC)
    elif op == 0xF:
      func_jump_and_link(op,d,s,t,memory,register, PC)
    else:
      show_memory(memory)
      print "Error: Unknown opcode ({}), aborting!".format(op)
      return -1

  print "Final memory configuration:"
  show_memory(memory)
  return 0

#Run main() if this script is invoked directly.
#Afterwards the return value of main() will be the return value of the script
if __name__ == "__main__":
  sys.exit(main())