##############################################################################
# This Python module is a companion to 'TMulator.py', providing additional
# programs to run (along with tapes and starting positions). They are
# imported into the main program, such that they are available for being chosen
#
# To configure the machine to run the desired program on the desired tape at the desired
# starting cell, a few minor hand-hacks are required by the user, in order to set the values of the
# following variables, within the main section of 'TMulator.py':
#
# state_machine = PROGRAM_08          # <------------------------------------------------------    Choose here the program you wish to run
# current_tape = TAPE_02; current_tape_index = START_CELL_INDEX_02  # <------------------------------      Choose desired tape and start cell index
#
# This code has been written in Python 3.8.0 (but should be compatible with earlier versions of Python3)
#
# License:
# MIT License (see https://github.com/deebs67/TMulator/blob/master/LICENSE)
#
# Copyright (c) 2020 deebs67
#

##############################################################################
# Programs (state-machine descriptions)
##############################################################################
#
# Write a (state machine) program in terms of 'cards' (one for each state), which defines the 'program'. For the top-level dict, the
# key is the state, and the value is a card for that state (itself represented as a dict of dicts, keyed by current symbol on the tape,
# where the inner dicts are the corresponding value, which define  the 'actions' to take, given that symbol on the tape).
# The halting state is 0, which doesn't need a card to be defined for it, so we just make a placemarker card for card 0
PROGRAM_01 =    { # This program takes a binary number enclosed in blanks, starting on the LHS blank, and increments that binary number by 1, perhaps overwriting the LHS blank with a 1 (if the input was all 1's)
                    0: 'Placemarker card for halting state 0',
                    1:  { # Starting state - it should be sitting on the LHS blank, otherwise stop, there must be an error
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and move to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Write 'E' (for error) and stop
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}     # Write 'E' (for error) and stop
                        }, 
                    2:  {  # This the state which searches for the RHS blank, then steps 1 left and enters state 3, to do the actual incrementing
                            '_': { 'write': '_', 'step': -1, 'next_state': 3},  # We've found the blank, re-write it, step left and enter state 3
                            0: { 'write': 0, 'step': +1, 'next_state': 2},   # Keep moving right and stay in this state
                            1: { 'write': 1, 'step': +1, 'next_state': 2}   # Keep moving right and stay in this state 
                        },
                    3:  {  # State which actually does the incrementing
                            '_': { 'write': 1, 'step': 0, 'next_state': 0},  # If we hit the LHS blank, write a 1 and halt
                            0: { 'write': 1, 'step': 0, 'next_state': 0},   # Change 0 to 1 and halt
                            1: { 'write': 0, 'step': -1, 'next_state': 3}   # Change 1 to 0 and move left, looking to increment the next more significant bit 
                        },                        
                }

PROGRAM_02 =    { # This program takes a binary number enclosed in blanks, starting on the LHS blank, and flips every binary bit (so it is a NOT gate separately on every bit)
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and start the main bit flipping operation (state 2)
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # In this state we step over every binary digit, and flip it
                            '_': { 'write': '_', 'step': 0, 'next_state': 0},  # We must be on the RHS blank so halt
                            0: { 'write': 1, 'step': +1, 'next_state': 2},   # Flip the bit, step right, stay in this state
                            1: { 'write': 0, 'step': +1, 'next_state': 2}   # Flip the bit, step right, stay in this state
                        },                       
                }

PROGRAM_03 =    { # This program acts as an AND gate for the two bits enclosed in blanks
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and start the logic operation (state 2)
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # In this state we start the logic operation, looking at the first bit
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Expecting a 1 or a 0, Error - write 'E' and halt
                            0: { 'write': 0, 'step': +3, 'next_state': 3},   # Result must be 0, so jump to where to write that
                            1: { 'write': 1, 'step': +1, 'next_state': 4}   # Re-write the bit, step right, stay in this state
                        }, 
                    3:  { # The result has been decided as 0, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': '0', 'step': 0, 'next_state': 0},  # Write the 0, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                        },
                    4:  { # Now we examine the second bit, having decided that the first bit was a 1
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Expecting a 1 or a 0, Error - write 'E' and halt
                            0: { 'write': 0, 'step': +2, 'next_state': 3},   # Result must be 0, so jump to where to write that
                            1: { 'write': 1, 'step': +2, 'next_state': 5}   # Result must be 1, so jump to where to write that
                        },
                    5:  { # The result has been decided as 1, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': '1', 'step': 0, 'next_state': 0},  # Write the 1, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                        },                   
                }

PROGRAM_04 =    { # This program acts as an OR gate for the two bits enclosed in blanks
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and start the logic operation (state 2)
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # In this state we start the logic operation, looking at the first (LHS) bit
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Expecting a 1 or a 0, Error - write 'E' and halt
                            0: { 'write': 0, 'step': +1, 'next_state': 3},   # Re-write the bit, step right, goto state for RHS bit
                            1: { 'write': 1, 'step': +3, 'next_state': 5}   # Result must be 1, so jump to where to write that
                        }, 
                    3:  { # Examine the RHS bit, given that the LHS bit was 0
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Not expecting '_', so Error and halt
                            0: { 'write': 0, 'step': +2, 'next_state': 4},   # Result must be 0, so jump to where to write that
                            1: { 'write': 1, 'step': +2, 'next_state': 5},   # Result must be 1, so jump to where to write that
                        },
                    4:  { # The result has been decided as 0, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': 0, 'step': 0, 'next_state': 0},  # Write the 0, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Expecting '_', so Error and halt
                        },
                    5:  { # The result has been decided as 1, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': 1, 'step': 0, 'next_state': 0},  # Write the 1, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                        },                   
                }

PROGRAM_05 =    { # This program acts as an XOR gate for the two bits enclosed in blanks
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and start the logic operation (state 2)
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # In this state we start the logic operation, looking at the first (LHS) bit
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Expecting a 1 or a 0, Error - write 'E' and halt
                            0: { 'write': 0, 'step': +1, 'next_state': 3},   # Re-write the bit, step right, goto state for checking RHS bit given that LHS bit was 0
                            1: { 'write': 1, 'step': +1, 'next_state': 4}   # Re-write the bit, step right, goto state for checking RHS bit given that LHS bit was 1
                        }, 
                    3:  { # Examine the RHS bit, given that the LHS bit was 0
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Not expecting '_', so Error and halt
                            0: { 'write': 0, 'step': +2, 'next_state': 5},   # Result must be 0, so jump to where to write that
                            1: { 'write': 1, 'step': +2, 'next_state': 6},   # Result must be 1, so jump to where to write that
                        },
                    4:  { # Examine the RHS bit, given that the LHS bit was 1
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Not expecting '_', so Error and halt
                            0: { 'write': 0, 'step': +2, 'next_state': 6},   # Result must be 1, so jump to where to write that
                            1: { 'write': 1, 'step': +2, 'next_state': 5},   # Result must be 0, so jump to where to write that
                        },
                    5:  { # The result has been decided as 0, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': 0, 'step': 0, 'next_state': 0},  # Write the 0, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                        },
                    6:  { # The result has been decided as 1, so write this and halt (we are expecting to overwrite a blank)
                            '_': { 'write': 1, 'step': 0, 'next_state': 0},  # Write the 1, then halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Expecting '_', so Error and halt
                        },                  
                }

PROGRAM_06 =    { # This program copies a 4-bit binary number 5 cells over to the right
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and start the copy operation (state 2)
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # The basic read operation, until we hit the RHS blank
                            '_': { 'write': '_', 'step': 0, 'next_state': 0},  # We've found the RHS blank, so halt
                            0: { 'write': 0, 'step': +5, 'next_state': 3},   # Re-write the bit, and jump to where we will copy it
                            1: { 'write': 1, 'step': +5, 'next_state': 4}   # Re-write the bit, and jump to where we will copy it
                        }, 
                    3:  { # Copy a 0 symbol
                            '_': { 'write': 0, 'step': -4, 'next_state': 2},  # Write a 0 symbol, and jump back to next bit
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                        },
                    4:  { # Copy a 1 symbol
                            '_': { 'write': 1, 'step': -4, 'next_state': 2},  # Write a 1 symbol, and jump back to next bit
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                        },             
                }

PROGRAM_07 =    { # This program adds together two unary numbers separated by a single blank, simply by setting the blank to 1, and blanking the rightmost 1
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step right off the blank (error if blank not found) and step over the first unary number
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right off the blank, and go to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error - write 'E' and halt
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # Error - write 'E' and halt
                        },
                    2:  { # Step over the first unary number, until we hit the linking blank
                            '_': { 'write': 1, 'step': +1, 'next_state': 3},  # We've found the RHS blank, so put a 1 there, and move to the second number
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   #  Error (we shouldn't see a 0) - write 'E' and halt
                            1: { 'write': 1, 'step': +1, 'next_state': 2}   # Re-write the bit, and step to the right, same state
                        }, 
                    3:  { # Step over the second unary number, until we hit the RHS blank
                            '_': { 'write': '_', 'step': -1, 'next_state': 4},  # Overwrite the blank, step left
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   #  Error (we shouldn't see a 0) - write 'E' and halt
                            1: { 'write': 1, 'step': +1, 'next_state': 3},   # Re-write the bit, and step to the right, same state
                        },
                    4:  { # Blank the final 1, to compensate for the linking blank which we set to 1
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Error (we shouldn't see a '_') - write 'E' and halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Error (we shouldn't see a 0) - write 'E' and halt
                            1: { 'write': '_', 'step': 0, 'next_state': 0},   # Write the blank, and halt
                        },             
                }

PROGRAM_08 =    { # This program takes a binary number enclosed in blanks, starting on the LHS blank, and decrements that binary number by 1, but gives an error if the number is all 0s
                    0: 'Placemarker card for halting state 0',
                    1:  { # Starting state - it should be sitting on the LHS blank, otherwise stop, there must be an error
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and move to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Write 'E' (for error) and stop
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}     # Write 'E' (for error) and stop
                        }, 
                    2:  {  # This the state which searches for the RHS blank, then steps 1 left and enters state 3, to do the actual decrementing
                            '_': { 'write': '_', 'step': -1, 'next_state': 3},  # We've found the blank, re-write it, step left and enter state 3
                            0: { 'write': 0, 'step': +1, 'next_state': 2},   # Keep moving right and stay in this state
                            1: { 'write': 1, 'step': +1, 'next_state': 2}   # Keep moving right and stay in this state 
                        },
                    3:  {  # State which actually does the decrementing
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # If we hit the LHS blank, then there is an error
                            0: { 'write': 1, 'step': -1, 'next_state': 3},   # Change to a 1, step left
                            1: { 'write': 0, 'step': 0, 'next_state': 0}   # Change 1 to 0 and halt 
                        },                        
                }

PROGRAM_09 =    { # This program takes a two 2-bit binary numbers separated by a blank, and detects whether or not they are equal (writes a 1 if they are equal, 0 otherwise)
                    0: 'Placemarker card for halting state 0',
                    1:  { # Starting state - it should be sitting on the LHS blank, otherwise stop, there must be an error
                            '_': { 'write': '_', 'step': +1, 'next_state': 2},  # Step right of the blank, and move to state 2
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # Write 'E' (for error) and stop
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}     # Write 'E' (for error) and stop
                        }, 
                    2:  {  # Read MS-bit of LHS binary word
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Write 'E' (for error) and stop
                            0: { 'write': 0, 'step': +3, 'next_state': 3},   # Jump to corresponding bit in RHS word
                            1: { 'write': 1, 'step': +3, 'next_state': 4}   # Jump to corresponding bit in RHS word 
                        },
                    3:  {  # Read MS-bit of RHS binary word, given that corresponding bit of LHS word was 0
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # If we hit a blank, then there is an error
                            0: { 'write': 0, 'step': -2, 'next_state': 5},   # This matches, now consider LS-bit
                            1: { 'write': 1, 'step': +3, 'next_state': 8}   # It differs, so the words differ - need to write a 0 in the output cell, then halt
                        },
                    4:  {  # Read MS-bit of RHS binary word, given that corresponding bit of LHS word was 1
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # If we hit a blank, then there is an error
                            0: { 'write': 0, 'step': +3, 'next_state': 8},   # It differs, so the words differ - need to write a 0 in the output cell, then halt
                            1: { 'write': 1, 'step': -2, 'next_state': 5}   # This matches, now consider LS-bit
                        },
                    5:  {  # Read LS-bit of LHS binary word
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # Write 'E' (for error) and stop
                            0: { 'write': 0, 'step': +3, 'next_state': 6},   # Jump to corresponding bit in RHS word
                            1: { 'write': 1, 'step': +3, 'next_state': 7}   # Jump to corresponding bit in RHS word 
                        },
                    6:  {  # Read LS-bit of RHS binary word, given that corresponding bit of LHS word was 0
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # If we hit a blank, then there is an error
                            0: { 'write': 0, 'step': +2, 'next_state': 9},   # This matches, so the words match - need to write a 1 in the output cell, then halt
                            1: { 'write': 1, 'step': +2, 'next_state': 8}   # It differs, so the words differ - need to write a 0 in the output cell, then halt
                        },
                    7:  {  # Read LS-bit of RHS binary word, given that corresponding bit of LHS word was 1
                            '_': { 'write': 'E', 'step': 0, 'next_state': 0},  # If we hit a blank, then there is an error
                            0: { 'write': 0, 'step': +2, 'next_state': 8},   # It differs, so the words differ - need to write a 0 in the output cell, then halt
                            1: { 'write': 1, 'step': +2, 'next_state': 9}   # This matches, so the words match - need to write a 1 in the output cell, then halt
                        },
                    8:  {  # The words differed, so write a 0 and halt
                            '_': { 'write': 0, 'step': 0, 'next_state': 0},  # Write a 0 and halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # If we hit a blank, then there is an error
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # If we hit a blank, then there is an error
                        },
                    9:  {  # The words matched, so write a 1 and halt
                            '_': { 'write': 1, 'step': 0, 'next_state': 0},  # Write a 1 and halt
                            0: { 'write': 'E', 'step': 0, 'next_state': 0},   # If we hit a blank, then there is an error
                            1: { 'write': 'E', 'step': 0, 'next_state': 0}   # If we hit a blank, then there is an error
                        },                                                
                }


##############################################################################
# Tapes (and starting-cell indices)
##############################################################################
#
# Define the tape starting condition and start cell index
TAPE_01 = ['_', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_01 = 0  # For writing a blank at the end of a line of 1's
TAPE_02 = ['_', 1, 0, 0, 0, '_', 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_02 = 0   # For the binary incrementer, decrementor or binary bit flipper
TAPE_03 = ['_', 1, 1, '_', '_', '_', 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_03 = 0   # For testing a logic gates (e.g. AND, OR etc.). Result over-written in middle if the 3 RHS blanks
TAPE_04 = ['_', 1, 0, 0, 0, '_', '_', '_', '_', '_', '_', 0, 0, 0, 0]; START_CELL_INDEX_04 = 0   # For copying a 4-bit binary number
TAPE_05 = ['_', 1, 1, 1, 1, '_', 1, 1, 1, 1, 1, '_', 0, 0, 0]; START_CELL_INDEX_05 = 0   # For adding two unary numbers separated by a blank
TAPE_06 = ['_', 0, 0, '_', 1, 0, '_', '_', '_', 0 ]; START_CELL_INDEX_06 = 0   # Detect if two 2-bit binary numbers are equal or not, write 1 if they are, 0 otherwise, in middle if the 3 RHS blanks
