#!/usr/bin/env python3
"""Calculate term frequency."""

import string
import sys


def swap(arr, fst_idx, snd_idx):
    """
    Swaps array entries.
    """
    arr[fst_idx], arr[snd_idx] = arr[snd_idx], arr[fst_idx]


# list of [word, frequency] pairs
WORD_FREQS = []
# list of stop words
with open('../stop_words.txt') as f:
    STOP_WORDS = f.read().split(',')
STOP_WORDS.extend(list(string.ascii_lowercase))

for line in open(sys.argv[1]):
    start_char = None
    i = 0
    for c in line:
        if start_char is None:
            if c.isalnum():
                # Start of a word
                start_char = i
        else:
            if not c.isalnum():
                # End of a word.
                found = False
                word = line[start_char:i].lower()
                # Ignore stop words.
                if word not in STOP_WORDS:
                    pair_index = 0
                    # Exists already?
                    for pair in WORD_FREQS:
                        if word == pair[0]:
                            pair[1] += 1
                            found = True
                            break
                        pair_index += 1
                    if not found:
                        WORD_FREQS.append([word, 1])
                    elif len(WORD_FREQS) > 1:
                        for n in reversed(range(pair_index)):
                            if WORD_FREQS[pair_index][1] > WORD_FREQS[n][1]:
                                swap(WORD_FREQS, n, pair_index)
                                pair_index = n
                start_char = None
        i += 1

for tf in WORD_FREQS[0:25]:
    print(tf[0], '-', tf[1])
