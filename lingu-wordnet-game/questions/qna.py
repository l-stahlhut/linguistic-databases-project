import random

import nltk
from typing import Dict, List




class QNA:
    """
    The QNA class serves as a base class for Q&A paris. The class knows its question type and will create the
    question-answer paris accordingly.
    """

    def __init__(self, q_type: str, num_wrong_answers: int) -> object:
        if q_type != 'definition' and q_type != 'relation' and q_type != 'true_false':
            raise Warning(f'{q_type} q type does not exist')
        else:
            self.q_type = q_type
        if q_type == 'true_false':
            self.num_wrong_answers = 1
        else:
            self.num_wrong_answers = num_wrong_answers

    def create_questions_answer_pairs(self, key_words, wrong_words) -> dict:
        """
        Function that calls a questions-answer pair creation function depending on the question type
        :param key_words: words
        :param wrong_words:
        :return: dict of Q&A pairs
        """
        if self.q_type == 'definition':
            qa_pairs = self._create_definition_qas(key_words, wrong_words)
        # TODO: add more question types and create QA pairs for them
        elif self.q_type == 'relation':
            qa_pairs = self._create_relation_qas(key_words, wrong_words)
        else:
            qa_pairs = self._create_true_false_qas(key_words, wrong_words)

        return qa_pairs

    def _create_true_false_qas(self, key_words, wrong_words):
        """
        create the true-false questions. Keeps track of what the correct answer is.
        :param key_words: dict of scraped word and its synset
        :return: dict of Q&A pairs including the index of the correct answer
        """
        qna_pairs = {}

        for w in key_words.items():
            # parse synset
            syn = NounSynset(w[1])

            # create correct solution
            solution_pair = syn.get_random_relation()
            solution_category = list(solution_pair.keys())[0]
            solution_word = list(solution_pair.values())[0]

            # create wrong solutions
            categories = ["Synonym", "Antonym", "Hyponym", "Hypernym", "Meronym", "Holonym"]
            random_category = random.choice(categories)

            question = "The word '{}' is a(n) {} of '{}' ({}).".format(syn.word, random_category, solution_word,
                                                                       syn.definition)
            if random_category == solution_category:
                a = (0, "True", ["True", "False"], (solution_word, syn.word, solution_category))
            else:
                a = (1, "False", ["True", "False"], (solution_word, syn.word, solution_category))

            qna_pairs[question] = a

        return qna_pairs

    def _create_relation_qas(self, key_words, wrong_words):
        """
        create the relation questions and the wrong answers. Shuffles questions and keeps track of
        what is the correct answer.
        :param key_words: dict of correct word and its synset
        :return: dict of Q&A pairs including the index of the correct answer
        """
        qna_pairs = {}
        # iterate through number of questions (number of synsets)
        for w in key_words.items():
            # parse synset so we get access to relation types
            syn = NounSynset(w[1])

            # create correct solution
            solution_pair = syn.get_random_relation()
            solution_category = list(solution_pair.keys())[0]
            solution_word = list(solution_pair.values())[0]

            # create wrong solutions
            wrong_categories = ["Synonym", "Antonym", "Hyponym", "Hypernym", "Meronym", "Holonym"]
            wrong_categories.remove(solution_category)
            # set the number of wrong answers
            wrong_categories = random.sample(wrong_categories, self.num_wrong_answers)

            question = "The word '{}' is a(n) ________ of '{}' ({}).".format(solution_word, syn.word, syn.definition)

            # if num wrong ans equals 3, gives me either 0, 1, 2, 3
            # --> corresponds to the indices of answers if there is one correct answer
            ind_of_correct_answer = random.randint(0, self.num_wrong_answers)

            # insert correct answers to wrong answers at specified index
            wrong_categories.insert(ind_of_correct_answer, solution_category)
            wrong_categories = (ind_of_correct_answer, (solution_word, syn.word, solution_category), wrong_categories)

            qna_pairs[question] = wrong_categories

        return qna_pairs


    def _create_definition_qas(self,
                               key_words: Dict[str, nltk.corpus.reader.wordnet.Synset],
                               wrong_words: Dict[str, nltk.corpus.reader.wordnet.Synset]) \
            -> dict:

        """
        create the definition questions and the wrong answers. Shuffles questions and keeps track of
        what is the correct answer.
        :param key_words: dict of correct word and its synset
        :param wrong_words: dict words for wrong answers and their synsets
        :return: dict of Q&A pairs including the index of the correct answer
        """

        qna_pairs = {}

        wrong_word_gen = (v for (k, v) in wrong_words.items())

        for corr_word in key_words:
            question = f"What is the correct definition of: {corr_word}"
            correct_definition = key_words[corr_word].definition()
            answers = []

            counter = 0
            while counter < self.num_wrong_answers:
                answers.append(next(wrong_word_gen).definition())
                counter += 1

            # if num wrong ans equals 3, gives me either 0, 1, 2, 3
            # --> corresponds to the indices of answers if there is one correct answer
            ind_of_correct_answer = random.randint(0, self.num_wrong_answers)

            # insert correct answers to wrong answers at specified index
            answers.insert(ind_of_correct_answer, correct_definition)

            answers = (ind_of_correct_answer, corr_word, answers)

            qna_pairs[question] = answers

        return qna_pairs


class NounSynset():
    """Create data type for nouns so that relations can be called."""

    def __init__(self, syn):
        self.synset = syn
        self.word = syn.lemmas()[0].name()
        self.name = syn.name()
        self.lemmas = syn.lemmas()
        self.definition = syn.definition()
        self.examples = syn.examples()
        self.synonyms = self.get_synonyms()
        self.antonyms = self.get_antonyms()
        self.hyponyms = self.get_hyponyms()
        self.hypernyms = self.get_hypernyms()
        self.meronyms = self.get_meronyms()
        self.holonyms = self.get_holonyms()

    def get_synonyms(self):
        """Words that belong to one synset are viewed as synonyms here.
        Returns a list of synonyms or an empty list if there are no synonyms."""
        synonyms = [l.name() for l in self.lemmas]
        synonyms.remove(self.word)

        return synonyms

    def get_antonyms(self):
        """Returns a list of antonyms or an empty list if there are no antonyms."""
        antonyms = []
        for l in self.lemmas:
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

        return antonyms

    def get_hyponyms(self):
        """Grabs words listed as direct hyponym.
        Returns a list of hyponyms or an empty list if there are no hyponyms."""
        if self.synset.hyponyms():
            hyponyms = [h.name() for h in self.synset.hyponyms()[0].lemmas()]
            return hyponyms
        else:

            return []

    def get_hypernyms(self):
        """Grabs words listed as direct hypernym.
        Returns a list of hypernyms or an empty list if there are no hypernyms."""
        if self.synset.hypernyms():
            hypernyms = [h.name() for h in self.synset.hypernyms()[0].lemmas()]
            return hypernyms
        else:
            return []

    def get_meronyms(self):
        """Grabs words listed as direct meronym.
        Returns a list of meronyms or an empty list if there are no meronym."""
        if self.synset.part_meronyms():
            meronyms = [h.name() for h in self.synset.part_meronyms()[0].lemmas()]
            return meronyms
        else:

            return []

    def get_holonyms(self):
        """Grabs words listed as direct holonym.
        Returns a list of holonyms or an empty list if there are no holonyms."""
        if self.synset.member_holonyms():
            holonyms = [h.name() for h in self.synset.member_holonyms()[0].lemmas()]
            return holonyms
        else:

            return []

    def non_empty_relations(self):
        """Returns a ditctionary with all relations of the synset."""
        relations = {}
        if len(self.synonyms) > 0:
            relations['Synonym'] = self.synonyms
        if len(self.antonyms) > 0:
            relations['Antonym'] = self.antonyms
        if len(self.hyponyms) > 0:
            relations['Hyponym'] = self.hyponyms
        if len(self.hypernyms) > 0:
            relations['Hypernym'] = self.hypernyms
        if len(self.meronyms) > 0:
            relations['Meronym'] = self.meronyms
        if len(self.holonyms) > 0:
            relations['Holonym'] = self.holonyms

        return relations

    def get_random_relation(self):
        """Returns a dictionary with a random category-relation pair for the synset."""
        relations = self.non_empty_relations()

        # case 1: there is only one relation category present for this synset
        if len(relations) == 1:
            category = (list(relations)[0])
            # 1a) there is only one option for this category (e.g. only 1 synonym)
            if len(relations[category]) == 1:
                solution = relations[category][0]
            # 1b) there are mulitple options for this category (e.g. only 2 synonyms)
            elif len(relations[category]) > 1:
                solution = random.choice(relations[category])
        # case 2: there are multiple relation categories present for this synset (e.g. synonyms, holonyms)
        elif len(relations) > 1:
            category = random.choice(list(relations.keys()))
            # 2a) only one option in the randomly chosen category
            if len(relations[category]) == 1:
                solution = relations[category][0]
            # 2b) mulitple options in the randomly chosen category
            elif len(relations[category]) > 1:
                solution = random.choice(relations[category])

        random_relation = {category: solution}

        return random_relation