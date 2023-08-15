# Linguistic Word Game based on WordNet
UZH, Department Computational Linguistics
<br>Linguistic Databases Semester Project, 2022

*Group: Deborah Jakobi, Yining Wang, Laura Stahlhut*

# Game Implementation
In this folder, we present the implementation of the game. 

# How to run the code

Set up a virtual environment
```
$ python3 -m venv wngame-env
$ source wngame-env/bin/activate
```

Clone this repository to your machine. Then navigate to the following folder and install the dependencies:
```
$ git clone git@gitlab.uzh.ch:deborah.jakobi/linguistic-databases-project.git
$ cd linguistic-databases-project/lingu-wordnet-game
$ pip install .
```

Before running the code, build the package: 
```
$ python3 -m pip install --upgrade build
$ python3 -m build
```
Run the code like so: 
```
$ python3 lingu-wordnet-game/lingu-wordnet-game.py 
```

# Desciption of the game
We implemented three types of question based on relations and definitions of nouns synsets in WordNet.
<br>The three question types are:
- Multiple choice questions (noun definitions)
- Fill-in-the-blanks questions (noun relations)
- True-or-false questions (noun relations)

In the beginning, one can choose the type and number of questions to be generated, as well as the number of wrong 
answers to be displayed for the first two question types. 