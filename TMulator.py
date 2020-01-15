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
# Global module imports
##############################################################################
#
from TMulator_programming import *      # Import additional TM programs, tapes  and start cells from companion module
                                        # I don't normally like 'import *', but I think it is justifiable here.

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
    action_dict = current_card[scanned_symbol]
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

#
# Define the tape starting condition and start cell index
TAPE_00 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '_', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; START_CELL_INDEX_00 = 15 # For writing a blank at the end of a line of 1's

##############################################################################
# Main loop
##############################################################################
#
if __name__=='__main__':
    #
    # Choose and initialise the program (which may have come from 'TMulator_programming.py')
    state_machine = PROGRAM_00          # <------------------------------------------------------    Choose here the program you wish to run
    current_card_index = START_CARD_INDEX   # Should always be 1

    #
    # Choose and initialise the data (which may have come from 'TMulator_programming.py')
    current_tape = TAPE_00; current_tape_index = START_CELL_INDEX_00  # <------------------------------      Choose desired tape and start cell index
    
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


    