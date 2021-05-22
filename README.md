# TMulator
A Turing Machine emulator written in Python  
See also a version of this hosted on Replit (which can be run from a web browser): https://replit.com/@deebs67/TMulator  

# References
Inspiration has been drawn from references such as the ones at the following URLs:

https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf

https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/one.html

https://www.i-programmer.info/babbages-bag/23-turing-machines.html

https://www.youtube.com/watch?v=DILF8usqp7M

http://www.ams.org/publicoutreach/feature-column/fcarc-turing

http://www.aturingmachine.com/examples.php

http://www.aturingmachine.com/examplesSub.php

https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/four.html

# Turing Machine 'improvements'
We take a few liberties in the definition of 'Turing Machine' (TM). For example, we
allow 'jumps' of more (or less) than 1 tape cell location either side. For larger jumps
we are saving ourselves the considerable inconvenience and verbosity of the need to define
many intermediate states, which the 1-step TM would need to do if it wished to carry
out larger jumps. We also allow our TM to write out an 'E' symbol (and halt) if it
encounters an error condition.

# User configuration
To configure the machine to run the desired program on the desired tape at the desired
starting cell, a few minor hand-hacks are required by the user, in order to set the values of the
following variables, within main:

state_machine = PROGRAM_08          # <---------------------------------------    Choose here the program you wish to run
current_tape = TAPE_02; current_tape_index = START_CELL_INDEX_02  # <-------      Choose desired tape and start cell index

There are a number of additional programs and tapes in the companion imported file 'TMulator_programming.py'

# Language
This code has been written mostly in Python 3.8.0 (but should be compatible with at least some earlier versions of Python3 and, of course, later versions too)
 
