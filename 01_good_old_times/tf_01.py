#!/usr/bin/env python

"""Calculate term frequency."""

import os
import sys

def touchopen(filename, *args, **kwargs):
    """Utility for handling the intermediate 'secondary memory'"""
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close() # "touch" file
    return open(filename, *args, **kwargs)

# The constrained memory should have no more than 1024 cells
DATA = []
# We're lucky:
# The stop words are only 433 characters and the lines are all
# less than 80 characters, so we can use that knowledge to
# simplify the problem: we can have the stop words loaded in
# memory while processing one line of the input at a time.
# If these two assumptions didn't hold, the algorithm would
# need to be changed considerably.

# Overall strategy: (PART 1) read the input file, count the
# words, increment/store counts in secondary memory (a file)
# (PART 2) find the 25 most frequent words in secondary memory

# PART 1:
# - read the input file one line at a time
# - filter the characters, normalize to lower case
# - identify words, increment corresponding counts in file

# Load the list of stop words
STOP_WORDS_FILE = open('../stop_words.txt')
DATA = [STOP_WORDS_FILE.read(1024).split(',')] # DATA[0] holds the stop words
STOP_WORDS_FILE.close()

DATA.append([])    # DATA[1] is line (max 80 characters)
DATA.append(None)  # DATA[2] is index of the start_char of word
DATA.append(0)     # DATA[3] is index on characters, i = 0
DATA.append(False) # DATA[4] is flag indicating if word was found
DATA.append('')    # DATA[5] is the word
DATA.append('')    # DATA[6] is word,NNNN
DATA.append(0)     # DATA[7] is frequency

# Open the secondary memory
WORD_FREQS = touchopen('WORD_FREQS', 'rb+')
# Open the input file
INPUT_FILE = open(sys.argv[1], 'r')
# Loop over input file's lines
while True:
    DATA[1] = [INPUT_FILE.readline()]
    if DATA[1] == ['']: # end of input file
        break
    if DATA[1][0][len(DATA[1][0])-1] != '\n': # If it does not end with \n
        DATA[1][0] = DATA[1][0] + '\n' # Add \n
    DATA[2] = None
    DATA[3] = 0
    # Loop over characters in the line
    for c in DATA[1][0]: # elimination of symbol c is exercise
        if DATA[2] is None:
            if c.isalnum():
                # We found the start of a word
                DATA[2] = DATA[3]
        else:
            if not c.isalnum():
                # We found the end of a word. Process it
                DATA[4] = False
                DATA[5] = DATA[1][0][DATA[2]:DATA[3]].lower()
                # Ignore words with len < 2, and stop words
                if len(DATA[5]) >= 2 and DATA[5] not in DATA[0]:
                    # Let's see if it already exists
                    while True:
                        DATA[6] = str(WORD_FREQS.readline().strip(), 'utf-8')
                        if DATA[6] == '':
                            break
                        DATA[7] = int(DATA[6].split(',')[1])
                        # word, no white space
                        DATA[6] = DATA[6].split(',')[0].strip()
                        if DATA[5] == DATA[6]:
                            DATA[7] += 1
                            DATA[4] = True
                            break
                    if not DATA[4]:
                        WORD_FREQS.seek(0, 1) # Needed in Windows
                        WORD_FREQS.write(bytes("%20s,%04d\n" % (DATA[5], 1), 'utf-8'))
                    else:
                        WORD_FREQS.seek(-26, 1)
                        WORD_FREQS.write(bytes("%20s,%04d\n" % (DATA[5], DATA[7]), 'utf-8'))
                    WORD_FREQS.seek(0, 0)
                # Let's reset
                DATA[2] = None
        DATA[3] += 1
# We're done with the input file
INPUT_FILE.close()
WORD_FREQS.flush()

# PART 2
# Now we need to find the 25 most frequently occuring words.
# We don't need anything from the previous values in memory
del DATA[:]

# Let's use the first 25 entries for the top 25 words
DATA = DATA + [[]]*(25 - len(DATA))
DATA.append('') # DATA[25] is word,freq from file
DATA.append(0)  # DATA[26] is freq

# Loop over secondary memory file
while True:
    DATA[25] = str(WORD_FREQS.readline().strip(), 'utf-8')
    if DATA[25] == '': # EOF
        break
    DATA[26] = int(DATA[25].split(',')[1]) # Read it as integer
    DATA[25] = DATA[25].split(',')[0].strip() # word
    # Check if this word has more counts than the ones in memory
    for i in range(25): # elimination of symbol i is exercise
        if DATA[i] == [] or DATA[i][1] < DATA[26]:
            DATA.insert(i, [DATA[25], DATA[26]])
            del DATA[26] #  delete the last element
            break

for tf in DATA[0:25]: # elimination of symbol tf is exercise
    if len(tf) == 2:
        print(tf[0], '-', tf[1])
# We're done
WORD_FREQS.close()
