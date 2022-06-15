import random
from words import word_list
import requests
import json
import csv
import pandas as pd
moves = {   }
name = ""

stages = ["""
 ___
|   |
|   |
|   o
|  /|\\
|   |
|  / \\
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|  /|\\
|   |
|  / 
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|  /|\\
|   |
|   
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|  /|\\
|   
|  
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|  /|
|   
|  
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|   |
|   
|  
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   o
|   
|   
|  
|
|--------|
|        |
|________|
""",
"""
 ___
|   |
|   |
|   
|   
|   
|  
|
|--------|
|        |
|________|
""",

]

difficulty_lvls= {
    "1": 7,
    "2": 5,
    "3": 4
}

categories = {
    "1" :"https://random-word-form.herokuapp.com/random/animal",
    "2" : "https://random-word-form.herokuapp.com/random/adjective",
    "3" : "https://random-word-form.herokuapp.com/random/noun"
}


def print_scoreboard():
    df = pd.read_csv('scoreboard.csv')
    df = df.sort_values('highest',ascending=False)
    print(df)

def save_to_scoreboard(name, won, score):
        editing = False
        file = open("scoreboard.csv")
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
            if(row[0] == name and row[0] != "name"):
                if won:
                    row[1] = int(row[1]) + 1
                else:
                    row[2] = int(row[2]) + 1
                if int(row[4]) < score:
                    row[4] = score
                row[3] = int(float(row[3])) + score
                editing = True
        if not editing:
            row = [name, 0, 0, 0, 0]
            if won:
                row[1] = int(row[1]) + 1
            else:
                row[2] = int(row[2]) + 1
            row[3] = score
            row[4] = score
            rows.append(row)
        dfw = pd.DataFrame(rows)
        dfw.to_csv('scoreboard.csv', mode='w', index=False, header=False)
        

def get_word_from_word_list(word_list):
    word = random.choice(word_list)
    return word.upper()

def get_word(categories, word_category):
    return str(requests.get(categories[word_category]).content)[4:-3].upper()

def game(word, diff_lvl, name,lifelines):
    print(word)
    tries = diff_lvl
    word_placeholder = "_" * len(word)
    finished = False
    moves = []
    guessed = []
    moves.append( {
            "phrase": "",
            "tries": tries,
            "guessed": guessed,
        })
    while moves[-1]["tries"] > 0 and not finished:
        print(moves)
        print(stages[moves[-1]["tries"]])
        print(word_placeholder)
        print("Press 1 to use a lifeline - undo previeus move (1 time)")
        print("Press 2 to use a lifeline - get random letter (1 time)")
        guess = input("Enter letter or a word: ").upper()
        if(len(guess) == 1): #wprowadzona litere
            if(guess.isnumeric()):
                 if(guess == "1" or guess == "2"):
                    if(guess == "1"):
                        if(lifelines[0]['used'] == False):
                            lifelines[0]['used'] = True
                            moves.pop()
                        else:
                            print("You have already used that")
                    if(guess == "2"):
                        if(lifelines[1]['used'] == False):
                            lifelines[1]['used'] = True
                            letter = random.choice(list(word))
                            while letter in moves[-1]["guessed"]:
                                letter = random.choice(list(word))
                            guessed.append(letter)
                            moves.append({
                                "phrase": letter,
                                "tries" : moves[-1]["tries"],
                                "guessed" : guessed
                            })
                        else: 
                            print("You have already used that")
            else:
                if guess in guessed:
                    print("You have alredy tried that..")
                elif guess not in word:
                    print("Unlucky :/")
                    
                    moves.append({
                        "phrase": guess,
                        "tries" : moves[-1]["tries"] - 1,
                        "guessed" : guessed
                        })
                else:
                    guessed.append(guess)
                    moves.append({
                        "phrase" : guess,
                        "tries" : moves[-1]["tries"],
                        "guessed" : guessed
                        })
                    #tutaj musimy sprawdzić jakie litery maja jakie indexy
                #Marta - i jak zgadniemy a to efektem koncowym bedzie
                #_a__a 
                #w tym celu
            i = 0 
            word_list = list(word_placeholder) # [_ _ _ ]
            for letter in word:
                if letter in guessed:
                    word_list[i] = letter
                i+=1
            word_placeholder = "".join(word_list)
            if(word_placeholder == word):
                guess = word
                score = int ((6 - diff_lvl) * (len(word)) * 37)
                finished = True
                save_to_scoreboard(name,True,score)
                print("You were right!")
                print("Your score is: " + str(score))
                # print("Your highest score is: " + )
        else:
            if(guess == word):
                #koniec
                score = int ((6 - diff_lvl) * (len(word)) * 37)
                finished = True
                save_to_scoreboard(name,True,score)
                print("You were right!")
                print("Your score is: " + str(score))
                # print("Your highest score is: " )
            elif(not guess.isnumeric()):
                moves.append( {
                    "phrase": "",
                    "tries": moves[-1]["tries"]-1,
                    "guessed": guessed,
                })
                print("Unlucky :/")
            
        if(moves[-1]["tries"] == 0):
            save_to_scoreboard(name,False,0)
            print(stages[0])
            print("You died. The word was: " + word)


def menu(name,lifelines):
    difficulty = ""
    word_category = ""
    choise =""
    while (choise != "1" and choise != "2"):
        print("1.Start game")
        print("2.Scoreboard")
        choise = input()
    if(choise == "1"):
        while (difficulty != "1" and difficulty != "2" and difficulty != "3"):
            print("Choose number between 1 and 3")
            print("Choose difficulty level:")
            print("1.Normal - 7 tries")
            print("2.Hard - 5 tries")
            print("3.Impossible - 4 tries")
            difficulty = input()

        load_words = ""
        while (load_words != "1" and load_words != "2"):
            print("1. Load from web")
            print("2. Load from text file")
            load_words = input()
        if(load_words == "1"):
            while (word_category != "1" and word_category != "2" and word_category != "3"):
                print("Choose number between 1 and 3")
                print("Choose category level:")
                print("1.Animal")
                print("2.Adjective")
                print("3.Nouns")
                word_category = input()
            word = get_word(categories, word_category)
        if(load_words == "2"):
            word = get_word_from_word_list(word_list)
        
        game(word,difficulty_lvls[difficulty],name,lifelines)

    if(choise == "2"):
        print_scoreboard()
end = ""
name = input("Enter your name: ")
while end != "q":
    guessed = []

    lifelines =  [{
        'id': 0,
        'name': 'undo last move',
        'used': False,
        },
        {
        'id': 1,
        'name': 'Random correct letter',
        'used': False,
        }
    ]

    menu(name,lifelines)
    end = input("Enter 'q' to end or anything else to play again: ")
