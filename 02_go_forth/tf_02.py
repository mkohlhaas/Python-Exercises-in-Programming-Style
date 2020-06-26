#!/usr/bin/python3
"""Calculate term frequency."""

import operator
import re
import string
import sys

#
# The all-important data stack
#
STACK = []

#
# The heap. Maps names to data (i.e. variables)
#
HEAP = {}


#
# The new "words" (procedures) of our program
#
def read_file():
    """
    Takes a path to a file on the stack and places the entire
    contents of the file back on the stack.
    """
    input_file = open(STACK.pop())
    STACK.append([input_file.read()])
    input_file.close()


def filter_chars():
    """
    Takes data on the stack and places back a copy with all
    nonalphanumeric chars replaced by white space.
    """
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. Push the pattern onto stack
    STACK.append(re.compile(r'[\W_]+'))
    # Push the result onto the stack
    STACK.append([STACK.pop().sub(' ', STACK.pop()[0]).lower()])


def scan():
    """
    Takes a string on the stack and scans for words, placing
    the list of words back on the stack
    """
    # Again, split() is too high-level for this style, but using
    # it for doing this fast and short. Left as exercise.
    STACK.extend(STACK.pop()[0].split())


def remove_stop_words():
    """
    Takes a list of words on the stack and removes stop words.
    """
    stop_words_file = open('../stop_words.txt')
    STACK.append(stop_words_file.read().split(','))
    stop_words_file.close()
    # add single-letter words
    STACK[-1].extend(list(string.ascii_lowercase))
    HEAP['stop_words'] = STACK.pop()
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    HEAP['words'] = []
    while len(STACK) > 0:
        if STACK[-1] in HEAP['stop_words']:
            STACK.pop()  # pop it and drop it
        else:
            HEAP['words'].append(STACK.pop())  # pop it, store it
    STACK.extend(HEAP['words'])  # Load the words onto the stack
    del HEAP['stop_words']  # Not needed
    del HEAP['words']


def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence.
    """
    HEAP['word_freqs'] = {}
    # A little flavour of the real Forth style here...
    while len(STACK) > 0:
        # ... but the following line is not in style, because the
        # naive implementation would be too slow
        if STACK[-1] in HEAP['word_freqs']:
            # Increment the frequency, postfix style: f 1 +
            STACK.append(HEAP['word_freqs'][STACK[-1]])  # push f
            STACK.append(1)  # push 1
            STACK.append(STACK.pop() + STACK.pop())  # add
        else:
            STACK.append(1)  # Push 1 in STACK[2]
        # Load the updated freq back onto the heap
        HEAP['word_freqs'][STACK.pop()] = STACK.pop()

    # Push the result onto the stack
    STACK.append(HEAP['word_freqs'])
    del HEAP['word_freqs']  # We don't need this variable anymore


def sort():
    """
    Sorts words according to frequency.
    """
    # Not in style, left as exercise
    STACK.extend(sorted(STACK.pop().items(), key=operator.itemgetter(1)))


if __name__ == "__main__":
    STACK.append(sys.argv[1])
    read_file()
    filter_chars()
    scan()
    remove_stop_words()
    frequencies()
    sort()

    STACK.append(0)
    # Check stack length against 1, because after we process
    # the last word there will be one item left
    while STACK[-1] < 25 and len(STACK) > 1:
        HEAP['i'] = STACK.pop()
        (WORD, WORD_FREQUENCY) = STACK.pop()
        print(WORD, '-', WORD_FREQUENCY)
        STACK.append(HEAP['i'])
        STACK.append(1)
        STACK.append(STACK.pop() + STACK.pop())
