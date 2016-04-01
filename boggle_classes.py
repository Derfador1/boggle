import random
import re

class Player:
    def __init__(self):
        self._score = 0
        self._guessed = []
    
    # point system for boggle
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
    # This board was chosen from 
    # www.bananagrammer.com/2013/10/
    # the-boggle-cude-redesign-and-its-effect.html
    # this version was the classic boggle version
    # made 1976-1986, I picked this version
    # because it is the most straight forward
    # simple version I have found
    die0 = ['a', 'a', 'c', 'i', 'o', 't']
    die1 = ['a', 'b', 'i', 'l', 't', 'y']
    die2 = ['a', 'b', 'j', 'm', 'o', 'q']
    die3 = ['a', 'c', 'd', 'e', 'm', 'p']
    die4 = ['a', 'c', 'e', 'l', 'r', 's']
    die5 = ['a', 'd', 'e', 'n', 'v', 'z']
    die6 = ['a', 'h', 'm', 'o', 'r', 's']
    die7 = ['b', 'i', 'f', 'o', 'r', 'x']
    die8 = ['d', 'e', 'n', 'o', 's', 'w']
    die9 = ['d', 'k', 'n', 'o', 't', 'u']
    die10 = ['e', 'e', 'f', 'h', 'i', 'y']
    die11 = ['e', 'g', 'k', 'l', 'u', 'y']
    die12 = ['e', 'g', 'i', 'n', 't', 'v']
    die13 = ['e', 'h', 'i', 'n', 'p', 's']
    die14 = ['e', 'l', 'p', 's', 't', 'u']
    die15 = ['g', 'i', 'l', 'r', 'u', 'w']
    #die15 = ['q', 'q', 'q', 'q', 'q', 'q']
    
    choices = {
        'zero':die0, 'one':die1, 'two':die2, 'three':die3, 
        'four':die4, 'five':die5, 'six':die6, 'seven':die7, 'eight':die8, 
        'nine':die9, 'ten':die10, 'eleven':die11, 'twelve':die12, 
        'thirteen':die13,'fourteen':die14, 'fifteen':die15
        }

    def __init__(self):
        self._graph = ""
        # gives me the letters from the 16 dice
        self._letter = [random.choice(i) for i in self.choices.values()]
        self._wordlist = ""
        
    def generate_graph(self, number):
        for item in self._letter:
            self._graph += str(item).lower()
            if number % 4 == 0:
                self._graph += ' '
            number += 1
        self._graph = self._graph.split()
    
    # gives me number of rows and columns    
    def row_col(self):
        self._num_rows = len(self._graph)
        self._num_cols = min(len(line) for line in self._graph)
    
    # used to print my game board on the curses screen  
    def print_graph(self, i, stdscr):    
        final = []
        check_list = []    

        number = 0
        for item in self._letter:
            if item == 'q':
                item = 'qu'
                final.append(item + " ")
            else:
                final.append(item + "  ") 
            number += 1
            check_list.append(item)
            if number % 4 == 0:
                check_list.append('\n')
                final_list = ''.join(final)
                stdscr.addstr(i + 1, 2, final_list)
                stdscr.refresh()
                i += 1
                final = []
        i += 4
        stdscr.refresh()
        return(i)

    # found the following code with a little seperate implementation on:
    # stackoverflow.com/questions/746082/
    # how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-
    # solver#750012   
        
    def get_words(self):
        self._alphabet = ''.join(set(''.join(self._graph)))
        if 'q' in self._alphabet:
            self._alphabet += 'u'
        self._words = re.compile('[' + self._alphabet + ']{3,}$', re.I).match
    
        self._possible_words = set(word.rstrip('\n') 
            for word in open('/usr/share/dict/words') 
                if self._words(word.lower()))
            
    def get_prefix(self):    
        self._prefixes = set(word[:i] 
            for word in self._possible_words for i in range(2, len(word) + 1))
    
    def solve(self):
        for y, row in enumerate(self._graph):
            for x, letter in enumerate(row):
                if letter == 'q':
                    letter = 'qu'
                for result in self.extending(letter, ((x, y),)):
                    yield result
        
    def extending(self, prefix, path):
        if prefix in self._possible_words:
            yield (prefix, path)
        for (nx, ny) in self.neighbors(path[-1]):
            if (nx, ny) not in path:
                if self._graph[ny][nx] == 'q':
                    prefix1 = prefix + 'qu'
                else:
                    prefix1 = prefix + self._graph[ny][nx]
                if prefix1 in self._prefixes:
                    for result in self.extending(prefix1, path + ((nx, ny),)):
                        yield result
    
    def neighbors(self, variable):
        x, y = variable
        for nx in range(max(0, x - 1), min(x+2, self._num_cols)):
            for ny in range(max(0, y - 1), min(y + 2, self._num_rows)):
                yield (nx, ny)
            
    def assemble_wordlist(self):
        self._wordlist = (' '.join(
            sorted(set(word for (word, path) in self.solve()))))
        # a seperate wordlist i use to save the unchanged wordlist
        self._full_wordlist = self._wordlist
