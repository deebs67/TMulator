##############################################################################
# This Python code has been written to emulate a simple Turing Machine.
# Inspiration has been drawn from references such as the following:
#
# https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/one.html
# https://www.i-programmer.info/babbages-bag/23-turing-machines.html
# https://www.youtube.com/watch?v=DILF8usqp7M
# http://www.ams.org/publicoutreach/feature-column/fcarc-turing
# http://www.aturingmachine.com/examples.php
# http://www.aturingmachine.com/examplesSub.php
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/four.html
#
# We take a few liberties in the definition of 'Turing Machine' (TM). For example, we
# allow 'jumps' of more (or less) than 1 tape cell location either side. For larger jumps
# we are saving ourselves the considerable inconvenience and verbosity of the need to define
# many intermediate states, which the 1-step TM would need to do if it wished to carry
# out larger jumps. We also allow our TM to write out an 'E' symbol (and halt) if it
# encounters an error condition.
#
# To configure the machine to run the desired program on the desired tape at the desired
# starting cell, a few minor hand-hacks are required by the user, in order to set the values of the
# following variables, within main:
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
# Turing Machine emulator function
##############################################################################
#
# Function to execute a step of the TM
def execute_a_TM_step(current_tape, current_tape_index, current_card):
    #
    # Make copies of the inputs we might want to change
    new_tape = current_tape
    new_tape_index = current_tape_index

    #
    # Read the current symbol
    scanned_symbol = new_tape[new_tape_index]
    #print('Scanned symbol:- ', scanned_symbol) #debug
    action_dict = current_card[scanned_symbol]
    #print('Action dict:- ',action_dict) #debug
    character_to_write = action_dict['write']
    step_size = action_dict['step']
    new_card_index = action_dict['next_state']

    #
    # Write to the tape
    new_tape[new_tape_index] = character_to_write

    #
    # Step the tape head
    new_tape_index += step_size

    #
    # Return the updated parameters
    return_tuple = (new_tape, new_tape_index, new_card_index)
    #print('Return tuple:- ', return_tuple) #debug
    return return_tuple


##############################################################################
# TM Initialisation and program/data options
##############################################################################
#
# Various top-level parameters
START_CARD_INDEX = 1        # We always start on card index 1, and stop (halt) on card index 0
MAX_NUMBER_OF_STEPS = 20    # Will take fewer steps if it halts earlier than this

#
# Write a (state machine) program in terms of 'cards' (one for each state), which defines the 'program'. For the top-level dict, the
# key is the state, and the value is a card for that state (itself represented as a dict of dicts, keyed by current symbol on the tape,
# where the inner dicts are the corresponding value, which define  the 'actions' to take, given that symbol on the tape).
# The halting state is 0, which doesn't need a card to be defined for it, so we just make a placemarker card for card 0

PROGRAM_00 =    { # This program replaces a zero with a blank to the right hand end of a line of 1s (of arbitrary length), and then simply halts
                    0: 'Placemarker card for halting state 0',
                    1:  { # In this state we step over every 1, re-writing it and stepping right
                            '_': { 'write': '_', 'step': +1, 'next_state': 1},  # Step right of the blank, and stay in this state
                            0: { 'write': '_', 'step': 0, 'next_state': 0},   # We must be off the RHS end. Write a blank and halt
                            1: { 'write': 1, 'step': +1, 'next_state': 1}   # Write a 1, step right and stay in this state
                        },   
                }

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


#
# Define the tape starting condition
TAPE_00 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '_', 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_00 = 15 # For writing a blank at the end of a line of 1's
TAPE_01 = ['_', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_01 = 0  # For writing a blank at the end of a line of 1's
TAPE_02 = ['_', 1, 1, 0, 0, '_', 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_02 = 0   # For the binary incrementer, decrementor or binary bit flipper
TAPE_03 = ['_', 1, 1, '_', '_', '_', 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_03 = 0   # For testing a logic gates (e.g. AND, OR etc.). Result over-written in middle if the 3 RHS blanks
TAPE_04 = ['_', 1, 0, 0, 0, '_', '_', '_', '_', '_', '_', 0, 0, 0, 0]; START_CELL_INDEX_04 = 0   # For copying a 4-bit binary number
TAPE_05 = ['_', 1, 1, 1, 1, '_', 1, 1, 1, 1, 1, '_', 0, 0, 0]; START_CELL_INDEX_05 = 0   # For adding two unary numbers separated by a blank


##############################################################################
# Main loop
##############################################################################
#
if __name__=='__main__':
    #
    # Choose and initialise the program
    state_machine = PROGRAM_08          # <------------------------------------------------------    Choose here the program you wish to run
    current_card_index = START_CARD_INDEX   # Should always be 1

    #
    # Choose and initialise the data
    current_tape = TAPE_02; current_tape_index = START_CELL_INDEX_02  # <------------------------------      Choose desired tape and start cell index
    
    #
    # Print out starting machine state
    print('\n\nSimple Turing Machine implementation')
    print('====================================\n')
    print('Initial starting state')
    print('\nState machine definition (i.e. the program):- \n', state_machine)
    print('\nCurrent tape (i.e. the input data):- ', current_tape)
    print('Current tape index (i.e. current R/W head position):- ', current_tape_index)    
    print('Current card index (i.e. current state):- ', current_card_index)

    #
    # Now step the machine through the desired maximum number of steps, or fewer if it halts earlier than that
    for time_step in range(1,MAX_NUMBER_OF_STEPS+1):
        #
        # Execute the step
        (new_tape, new_tape_index, new_card_index) = execute_a_TM_step(current_tape, current_tape_index, state_machine[current_card_index])
        #
        # Update state parameters now that we have executed the step
        current_tape = new_tape
        current_tape_index = new_tape_index
        current_card_index = new_card_index

        #
        # Print machine state after this time step
        print('\nTime step (just taken):- ', time_step)
        print('Current tape:- ', current_tape)
        print('Current tape index:- ', current_tape_index)
        print('Current card index:- ', current_card_index)

        #
        # Halt the machine if we have hit state 0
        if current_card_index == 0:
            print('\nMachine halted (on card index 0)\n')
            break


    