#!/usr/bin/python3
"""Calculate term frequency."""

import sys
import numpy as np

# Example input: "Hello  World!"
CHARACTERS = np.array([' '] + list(open(sys.argv[1]).read()) + [' '])
# Result: array([' ', 'H', 'e', 'l', 'l', 'o', ' ', ' ',
#           'W', 'o', 'r', 'l', 'd', '!', ' '], dtype='<U1')

# Normalize
CHARACTERS[~np.char.isalpha(CHARACTERS)] = ' '
CHARACTERS = np.char.lower(CHARACTERS)
# Result: array([' ', 'h', 'e', 'l', 'l', 'o', ' ', ' ',
#           'w', 'o', 'r', 'l', 'd', ' ', ' '], dtype='<U1')

### Split the words by finding the indices of spaces
SP = np.where(CHARACTERS == ' ')
# Result: (array([ 0, 6, 7, 13, 14], dtype=int64),)
# A little trick: let's double each index, and then take pairs
SP2 = np.repeat(SP, 2)
# Result: array([ 0, 0, 6, 6, 7, 7, 13, 13, 14, 14], dtype=int64)
# Get the pairs as a 2D matrix, skip the first and the last
W_RANGES = np.reshape(SP2[1:-1], (-1, 2))
# Result: array([[ 0,  6],
#                [ 6,  7],
#                [ 7, 13],
#                [13, 14]], dtype=int64)
# Remove the indexing to the spaces themselves
W_RANGES = W_RANGES[np.where(W_RANGES[:, 1] - W_RANGES[:, 0] > 2)]
# Result: array([[ 0,  6],
#                [ 7, 13]], dtype=int64)

# Voila! Words are in between spaces, given as pairs of indices
WORDS = list(map(lambda r: CHARACTERS[r[0]:r[1]], W_RANGES))
# Result: [array([' ', 'h', 'e', 'l', 'l', 'o'], dtype='<U1'),
#          array([' ', 'w', 'o', 'r', 'l', 'd'], dtype='<U1')]
# Let's recode the characters as strings
SWORDS = np.array(list(map(lambda w: ''.join(w).strip(), WORDS)))
# Result: array(['hello', 'world'], dtype='<U5')

# Next, let's remove stop words
STOP_WORDS = np.array(list(set(open('../stop_words.txt').read().split(','))))
NS_WORDS = SWORDS[~np.isin(SWORDS, STOP_WORDS)]

### Finally, count the word occurrences
UNIQ, COUNTS = np.unique(NS_WORDS, axis=0, return_counts=True)
WF_SORTED = sorted(zip(UNIQ, COUNTS), key=lambda t: t[1], reverse=True)

for WORDS, WORD_FREQUENCY in WF_SORTED[:25]:
    print(WORDS, '-', WORD_FREQUENCY)
