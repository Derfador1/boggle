#begining file
import random

class Player:
    def __init__(self):
        self._score = 0
        self._guessed = []
    
    def point(self, word):
        wordlen = len(word)
        if wordlen <= 4:
            self._score += 1
        elif wordlen == 5:
            self._score += 2
        elif wordlen == 6:
            self._score += 3
        elif wordlen == 7:
            self._score += 5
        else:
            self._score  += 11
            
class GameBoard:
    # This choice was based on basic hasboro dice setup
    # found on everything2.com/title/Boggle
    die0 = ['a', 'e', 'a', 'n', 'e', 'g']
    die1 = ['a', 'h', 's', 'p', 'c', 'o']
    die2 = ['a', 's', 'p', 'f', 'f', 'k']
    die3 = ['o', 'b', 'j', 'o', 'a', 'b']
    die4 = ['i', 'o', 't', 'm', 'u', 'c']
    die5 = ['r', 'y', 'v', 'd', 'e', 'l']
    die6 = ['l', 'r', 'e', 'i', 'x', 'd']
    die7 = ['e', 'i', 'u', 'n', 'e', 's']
    die8 = ['w', 'n', 'g', 'e', 'e', 'h']
    die9 = ['l', 'n', 'h', 'n', 'r', 'z']
    die10 = ['t', 's', 't', 'i', 'y', 'd']
    die11 = ['o', 'w', 't', 'o', 'a', 't']
    die12 = ['e', 'r', 't', 't', 'y', 'l']
    die13 = ['t', 'o', 'e', 's', 's', 'i']
    die14 = ['t', 'e', 'r', 'w', 'h', 'v']
    #die15 = ['n', 'u', 'i', 'h', 'm', 'q']
    die15 = ['q', 'q', 'q', 'q', 'q', 'q']
    
    choices = {
        'zero':die0, 'one':die1, 'two':die2, 'three':die3, 
        'four':die4, 'five':die5, 'six':die6, 'seven':die7, 'eight':die8, 
        'nine':die9, 'ten':die10, 'eleven':die11, 'twelve':die12, 
        'thirteen':die13,'fourteen':die14, 'fifteen':die15
        }

    def __init__(self):
        self._graph = ""
        self._letter = [random.choice(i) for i in self.choices.values()]
        self._wordlist = ""
        
        
    def generate_graph(self, number):    
        for item in self._letter:
            self._graph += str(item).lower()
            if number % 4 == 0:
                self._graph += ' '
            number += 1
        self._graph = self._graph.split()
        
    def row_col(self):
        self._num_rows = len(self._graph)
        self._num_cols = min(len(line) for line in self._graph)
        
    
        
