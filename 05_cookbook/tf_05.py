#!/usr/bin/python3
"""Calculate term frequency."""

import sys
import string


def read_file(path_to_file):
    """
    Load file into data
    """
    data = []
    with open(path_to_file) as input_file:
        data = data + list(input_file.read())
    return data


def filter_chars_and_normalize(data):
    """
    Replaces all nonalphanumeric chars in data with white space
    """
    for i, char in enumerate(data):
        if not char.isalnum():
            data[i] = ' '
        else:
            data[i] = data[i].lower()


def scan(data):
    """
    Scans data for words, filling the global variable WORDS
    """
    words = []
    data_str = ''.join(data)
    words = words + data_str.split()
    return words


def remove_stop_words(words):
    """
    Remove stop words and single letter words from WORDS
    """
    with open('../stop_words.txt') as stop_words_file:
        stop_words = stop_words_file.read().split(',')
    # single-letter words are also stop_words
    stop_words.extend(list(string.ascii_lowercase))
    indexes = []
    for i, word in enumerate(words):
        if word in stop_words:
            indexes.append(i)
    for i in reversed(indexes):
        words.pop(i)
    return words


def frequencies(words):
    """
    Creates a list of word and frequency pairs
    """
    word_freqs = []
    for word in words:
        keys = [wd[0] for wd in word_freqs]
        if word in keys:
            word_freqs[keys.index(word)][1] += 1
        else:
            word_freqs.append([word, 1])
    return word_freqs


def sort(word_freqs):
    """
    Sorts WORD_FREQS by frequency
    """
    word_freqs.sort(key=lambda x: x[1], reverse=True)
    return word_freqs


if __name__ == "__main__":
    INPUT_DATA = read_file(sys.argv[1])
    filter_chars_and_normalize(INPUT_DATA)
    WORDS = scan(INPUT_DATA)
    remove_stop_words(WORDS)
    WORD_FREQS = frequencies(WORDS)
    sort(WORD_FREQS)

    for tf in WORD_FREQS[0:25]:
        print(tf[0], '-', tf[1])
