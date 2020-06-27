#!/usr/bin/python3
"""Calculate term frequency."""

import functools
import operator
import re
import string
import sys

def compose(*functions):
    """
    Compose functions.
    """
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions,
                            lambda x: x)


def read_file(path_to_file):
    """
    Takes a path to a file and returns the entire
    contents of the file as a string
    """
    with open(path_to_file) as input_file:
        data = input_file.read()
    return data


def filter_chars_and_normalize(str_data):
    """
    Takes a string and returns a copy with all nonalphanumeric
    chars replaced by white space
    """
    pattern = re.compile(r'[\W_]+')
    return pattern.sub(' ', str_data).lower()


def scan(str_data):
    """
    Takes a string and scans for words, returning
    a list of words.
    """
    return str_data.split()


def remove_stop_words(word_list):
    """
    Takes a list of words and returns a copy with all stop
    words removed
    """
    with open('../stop_words.txt') as stop_words_file:
        stop_words = stop_words_file.read().split(',')
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    word_freqs = {}
    for word in word_list:
        if word in word_freqs:
            word_freqs[word] += 1
        else:
            word_freqs[word] = 1
    return word_freqs


def sort(word_freq):
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency
    """
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)


def print_all(word_freqs):
    """
    Takes a list of pairs where the entries are sorted by frequency and print them recursively.
    """
    if word_freqs:
        print(word_freqs[0][0], '-', word_freqs[0][1])
        print_all(word_freqs[1:])


if __name__ == "__main__":
    INPUT_FILE = sys.argv[1]
    if INPUT_FILE:
        WORD_FREQS = compose(
            read_file,
            filter_chars_and_normalize,
            scan,
            remove_stop_words,
            frequencies,
            sort)
        print_all(WORD_FREQS(INPUT_FILE)[0:25])
