#!/usr/bin/env python

import nltk
from random import sample

from typing import Dict

try:
    from nltk.corpus import wordnet as wn
    from nltk.corpus import words
    from nltk.corpus import brown
except LookupError:
    nltk.download("wordnet")
    nltk.download("punkt")  # tokenizer
    nltk.download('omw-1.4')  # open multilingual wordnet
    nltk.download('averaged_perceptron_tagger')
    nltk.download('words')
    from nltk.corpus import wordnet as wn
    from nltk.corpus import words
    from nltk.corpus import brown


class Scraper:

    def __init__(self):
        self.words = brown.words()
        self.freq_dist = nltk.FreqDist(brown.words())

    def get_random_words(self, number=5) -> Dict[str, nltk.corpus.reader.wordnet.Synset]:
        """
        this method returns a dict of (word, synset) pairs that are randomly sampled. It makes sure that all words have
        a synset in WordNet
        :param number: number of random words that exist in WordNet to return
        :return: dictionary of (word, synset) pairs
        """
        # TODO: possibly exclude stopwords and punctuation symbols
        words_except_freq = self.freq_dist.most_common()[10:len(self.freq_dist.most_common())//2]
        print(len(words_except_freq))

        words = {}

        # sample as many words as required
        while len(words) < number:
            word = sample(words_except_freq, 1)[0][0]

            synsets = {}
            possibilities = []
            for synset in wn.synsets(f'{word}'):

                # get only those synsets for the words, whose name is exactly the same as the word we use as query
                name = synset.name().split('.')[0]

                # for now we get only nouns and make sure that the word we get has the same name as the initial word
                # TODO: add adjectives, verbs
                if synset.pos() == 'n' and word in name:
                    possibilities.append(synset)

            # if the word that was randomly sampled is found int Wordnet, we add its synsets to our list
            # of possible synsets
            if possibilities:
                synsets[word] = possibilities
                # we sample one synset for each word
                words[word] = sample(synsets[word], 1)[0]

        return words

