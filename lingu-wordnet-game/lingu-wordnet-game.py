#!/usr/bin/env python

import argparse
import nltk

try:
    from nltk.corpus import wordnet as wn
    from nltk.corpus import words
except LookupError:
    nltk.download("wordnet")
    nltk.download("punkt")  # tokenizer
    nltk.download('omw-1.4')  # open multilingual wordnet
    nltk.download('averaged_perceptron_tagger')
    nltk.download('words')
    nltk.download('brown')
    from nltk.corpus import wordnet as wn

from game import Game


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
