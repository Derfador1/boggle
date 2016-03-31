import random
import re

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
        #stdscr.addstr(i, 0, self._wordlist) #remove later
        stdscr.refresh()
        #i += 10
        return(i)
        
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

    # found the following code with a little seperate implementation on:
    # stackoverflow.com/questions/746082/
    # how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-
    # solver#750012   
    
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
            
        self._full_wordlist = self._wordlist
