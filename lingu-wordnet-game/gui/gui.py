#!/usr/bin/env python

import random
import PySimpleGUI as sg


sg.theme('LightBrown1')


class GUI:

    def __init__(self):
        # TODO: add scoring function
        self.score = 0
        self.FONT = ('Helvetica', 14)

        waiting_layout = [
            [sg.Text('Please wait while we are creating the questions and preparing the game.'
                     '\nThis might take a while.')]
        ]
        self.waiting_window = sg.Window('Settings', waiting_layout, element_padding=5, font=self.FONT)

        final_layout = [
            [sg.Text('Thanks for playing with us!'
                     '\nYou can quit and start a new game if you would like.')],
            [sg.Button('Quit')]#, sg.Button('Start new game!')]
        ]

        self.final_window = sg.Window('Quit or restart?', final_layout, element_padding=5, font=self.FONT)

    def show_waiting_window(self, on: bool):
        if on:
            while True:
                event, value = self.waiting_window.read(timeout=1)
                if event == sg.TIMEOUT_EVENT:
                    break
        if not on:
            self.waiting_window.close()

    def show_final_window(self):
        while True:
            event, value = self.final_window.read(timeout=50000)
            if event == sg.TIMEOUT_EVENT:
                break
            # elif event == 'Start new game!':
            #    lingu_wordnet_game()
            elif event is None or event == 'Quit':
                break

        self.final_window.close()


    def get_settings(self) -> dict:
        """
        function to get settings from user for the game. Settings are questions types and how many wrong answers there
        should be for multiple choice questions.
        :return: dictionary with settings
        """

        layout = [
            [sg.Text('Please chose what settings you would like for playing the game. '
                     'Below, you can choose what question types you would like to play with.')],
            [sg.Checkbox('Definition questions:', default=True, key='def'),
             sg.Text('questions that ask you what definition of a specified word is correct.')],
            [sg.Checkbox('Relation questions:', default=False, key='rel'),
             sg.Text('questions that ask you about the relation of two words.')],
            [sg.Checkbox('True-false questions:', default=False, key='tf'),
             sg.Text('questions that ask you whether a specific statement concerning one or two words is correct.')],
            [sg.Text('Please choose the number of wrong answers there should be for multiple choice questions:')],
            [sg.Combo(values=[1, 2, 3, 4, 5],
                        default_value=3,
                        key='num_wrong_answers')],
            [sg.Text('How many questions of each type would you like to have:')],
            [sg.Combo(values=[1, 2, 3, 4, 5],
                        default_value=3,
                        key='num_questions')],
            [sg.Button('Ok')]
        ]

        settings_window = sg.Window('Settings', layout, element_padding=5, font=self.FONT)

        while True:
            event, values = settings_window.read()
            print(f"values={values}")
            print(f"event={event}")
            if event is None or event == 'Ok':
                break

        settings_window.close()

        return values

    def display_definition_questions(self, qas: dict, num_answers: int) -> None:
        """
        Displays questions form the game that are of type 'definition'.
        :param qas: dict consisting of key = question, and as values a tuple of
        format (index of correct answer, word that needs to be defined in the question, [all answers wrong and correct])
        :param num_answers: how many answers there are per question
        """

        # get questions an shuffle them
        questions = list(qas.keys())
        random.shuffle(questions)

        options = [str(i) + ')' for i in range(1, num_answers + 1)]

        for idx, q_str in enumerate(questions):
            answers = qas[q_str][2]
            word_to_define = qas[q_str][1]
            idx_correct_answer = qas[q_str][0]
            option_column = sg.Column([[sg.Checkbox(o, key=o), sg.Text(a)] for o, a in zip(options, answers)])

            layout = [
                [sg.Text(f'{q_str}')],
                [option_column],
                [sg.Button('Show solution')]
            ]

            window = sg.Window(f'Question {idx + 1}', layout, element_padding=5, font=self.FONT)

            # Event Loop to process "events" and get the "values" of the input
            while True:
                event, values = window.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Show solution':  # if user closes window or clicks cancel
                    break

            # close  the window
            window.close()

            # get the value that the user collected
            value = None
            for v in values:
                if values[v]:
                    value = v

            is_answer_correct = int(value[0]) - 1 == idx_correct_answer if value else 'none'

            solution_layout = [
                [sg.Text(f'You selected answer {value}') if value else sg.Text(f'You did not select an answer.')],
                [sg.Text(f'Your answer is correct!') if is_answer_correct
                 else sg.Text(f'Your answer is wrong')] if is_answer_correct != 'none' else [],
                [sg.Text(f'{word_to_define} means: {answers[idx_correct_answer]}')],
                [sg.Button('Next Question')]
            ]

            window_solution = sg.Window(f'Solution {idx + 1}', solution_layout, element_padding=5, font=self.FONT)
            print('You entered ', value)

            while True:
                event, values = window_solution.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Next Question':  # if user closes window or clicks cancel
                    break

            window_solution.close()

    def display_relationship_questions(self, qas: dict, num_answers: int) -> None:
        """
        Displays questions form the game that are of type 'definition'.
        :param qas: dict consisting of key = question, and as values a tuple of
        format (index of correct answer, word that needs to be defined in the question, [all answers wrong and correct])
        :param num_answers: how many answers there are per question
        """

        # get questions an shuffle them
        questions = list(qas.keys())
        random.shuffle(questions)

        options = [str(i) + ')' for i in range(1, num_answers + 1)]

        for idx, q_str in enumerate(questions):
            answers = qas[q_str][2]
            scraped_word, related_word, relation = qas[q_str][1]
            idx_correct_answer = qas[q_str][0]
            option_column = sg.Column([[sg.Checkbox(o, key=o), sg.Text(a)] for o, a in zip(options, answers)])

            layout = [
                [sg.Text(f'{q_str}')],
                [option_column],
                [sg.Button('Show solution')]
            ]

            window = sg.Window(f'Question {idx + 1}', layout, element_padding=5, font=self.FONT)

            # Event Loop to process "events" and get the "values" of the input
            while True:
                event, values = window.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Show solution':  # if user closes window or clicks cancel
                    break

            # close  the window
            window.close()

            # get the value that the user collected
            value = None
            for v in values:
                if values[v]:
                    value = v

            is_answer_correct = int(value[0]) - 1 == idx_correct_answer if value else 'none'

            solution_layout = [
                [sg.Text(f'You selected answer {value}') if value else sg.Text(f'You did not select an answer.')],
                [sg.Text(f'Your answer is correct!') if is_answer_correct
                 else sg.Text(f'Your answer is wrong')] if is_answer_correct != 'none' else [],
                [sg.Text(f'The word {scraped_word} is a(n) {answers[idx_correct_answer]} of {related_word}.')],  # TODO
                [sg.Button('Next Question')]
            ]

            window_solution = sg.Window(f'Solution {idx + 1}', solution_layout, element_padding=5, font=self.FONT)
            print('You entered ', value)

            while True:
                event, values = window_solution.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Next Question':  # if user closes window or clicks cancel
                    break

            window_solution.close()


    def display_true_false_questions(self, qas: dict):
        """
        Displays questions form the game that are of type 'definition'.
        :param qas: dict consisting of key = question, and as values a tuple of
        format (index of correct answer, word that needs to be defined in the question, [all answers wrong and correct])
        :param num_answers: how many answers there are per question
        """

        # get questions an shuffle them
        questions = list(qas.keys())
        random.shuffle(questions)

        options = [str(i) + ')' for i in range(1, 3)] #only two answers in this type

        for idx, q_str in enumerate(questions):
            scraped_word, related_word, relation = qas[q_str][3]
            answers = qas[q_str][2]
            correct_answer = qas[q_str][1]
            idx_correct_answer = qas[q_str][0]
            option_column = sg.Column([[sg.Checkbox(o, key=o), sg.Text(a)] for o, a in zip(options, answers)])

            layout = [
                [sg.Text(f'{q_str}')],
                [option_column],
                [sg.Button('Show solution')]
            ]

            window = sg.Window(f'Question {idx + 1}', layout, element_padding=5, font=self.FONT)

            # Event Loop to process "events" and get the "values" of the input
            while True:
                event, values = window.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Show solution':  # if user closes window or clicks cancel
                    break

            # close  the window
            window.close()

            # get the value that the user collected
            value = None
            for v in values:
                if values[v]:
                    value = v

            is_answer_correct = int(value[0]) - 1 == idx_correct_answer if value else 'none'

            solution_layout = [
                [sg.Text(f'You selected answer {value}') if value else sg.Text(f'You did not select an answer.')],
                [sg.Text(f'Your answer is correct!') if is_answer_correct
                 else sg.Text(f'Your answer is wrong')] if is_answer_correct != 'none' else [],
                [sg.Text(f'The word {related_word} is a(n) {relation} of {scraped_word}.')],  # TODO
                [sg.Button('Next Question')]
            ]

            window_solution = sg.Window(f'Solution {idx + 1}', solution_layout, element_padding=5, font=self.FONT)
            print('You entered ', value)

            while True:
                event, values = window_solution.read()
                print(f"values={values}")
                print(f"event={event}")
                if event is None or event == 'Next Question':  # if user closes window or clicks cancel
                    break

            window_solution.close()
