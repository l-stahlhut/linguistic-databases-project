#!/usr/bin/env python
import random
import pprint
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
    from nltk.corpus import wordnet as wn

from gui.gui import GUI
from scrape.scraper import Scraper
from questions.qna import QNA



class Game:

    def __init__(self):
        self.gui = GUI()
        self._get_settings_from_user()
        self.gui.show_waiting_window(True)

        self.scraper = Scraper()

        if self.definition:
            self.def_QNA = QNA('definition', self.num_wrong_answers)

        if self.relation:
            self.rel_QNA = QNA('relation', self.num_wrong_answers)

        if self.true_false:
            self.tf_QNA = QNA('true_false', self.num_wrong_answers)


    def start(self) -> None:
        """
        starts the actual game, goes though all question types and displays them to the user
        :return:
        """

        questions = self._create_questions()

        self.gui.show_waiting_window(False)
        if self.definition:
            self.gui.display_definition_questions(questions['def'], num_answers=self.num_wrong_answers+1)

        if self.relation:
            self.gui.display_relationship_questions(questions['rel'], num_answers=self.num_wrong_answers+1)

        if self.true_false:
            self.gui.display_true_false_questions(questions['tf'])

        self.gui.show_final_window()

    def _get_settings_from_user(self) -> None:
        """
        calls GUI to get the settings the user wants to play with
        :return: None
        """
        settings = self.gui.get_settings()

        self.definition = settings['def']
        self.relation = settings['rel']
        self.true_false = settings['tf']
        self.num_wrong_answers = settings['num_wrong_answers']
        self.num_questions = settings['num_questions']

    def _create_questions(self) -> dict:

        def_questions = {}
        rel_questions = {}
        tf_questions = {}

        if self.definition:
            key_words = self.scraper.get_random_words(number=self.num_questions)
            wrong_words = self.scraper.get_random_words(number=self.num_wrong_answers * self.num_questions)
            def_questions = self.def_QNA.create_questions_answer_pairs(key_words, wrong_words)

        if self.relation:
            key_words = self.scraper.get_random_words(number=self.num_questions)
            wrong_words = self.scraper.get_random_words(number=self.num_wrong_answers * self.num_questions)
            rel_questions = self.rel_QNA.create_questions_answer_pairs(key_words, wrong_words)

        if self.true_false:
            key_words = self.scraper.get_random_words(number=self.num_questions)
            wrong_words = self.scraper.get_random_words(number=self.num_wrong_answers * self.num_questions)
            tf_questions = self.tf_QNA.create_questions_answer_pairs(key_words, wrong_words)



        return {'def': def_questions, 'rel': rel_questions, 'tf': tf_questions}












