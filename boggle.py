#! /usr/bin/env python3

import time
import random
import sys
import os

import curses
#from curses.textpad import Textbox, rectangle
from itertools import permutations
import re

random.seed(time.time())

def stuff():
    begin_x = 1
    begin_y = 1
    height = 8
    width = 11
    box1 = curses.newwin(height, width, begin_y, begin_x)
    box1.box()
    box1.refresh()

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

def main(stdscr):
    # found the following code with a little seperate implementation on:
    # stackoverflow.com/questions/746082/
    # how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-
    # solver#750012
    
    letter = [random.choice(i) for i in choices.values()]
    number = 1
    i = 1
        
    graph = ""
    
    for item in letter:
        graph += str(item).lower()
        if number % 4 == 0:
            graph += ' '
        number += 1
    graph = graph.split()
    
    num_rows = len(graph)
    num_cols = min(len(line) for line in graph)
    
    alphabet = ''.join(set(''.join(graph)))
    #if 'q' in alphabet:
    #    alphabet += 'u'
    words = re.compile('[' + alphabet + ']{3,}$', re.I).match
    
    possible_words = set(word.rstrip('\n') 
        for word in open('/usr/share/dict/words') if words(word.lower()))
    prefixes = set(word[:i] 
        for word in possible_words for i in range(2, len(word) + 1))
    
    def solve():
        for y, row in enumerate(graph):
            for x, letter in enumerate(row):
                if letter == 'q':
                    letter = 'qu'
                for result in extending(letter, ((x, y),)):
                    yield result
        
    def extending(prefix, path):
        if prefix in possible_words:
            yield (prefix, path)
        for (nx, ny) in neighbors(path[-1]):
            if (nx, ny) not in path:
                if graph[ny][nx] == 'q':
                    prefix1 = prefix + 'qu'
                else:
                    prefix1 = prefix + graph[ny][nx]
                if prefix1 in prefixes:
                    for result in extending(prefix1, path + ((nx, ny),)):
                        yield result
    
    def neighbors(variable):
        x, y = variable
        for nx in range(max(0, x - 1), min(x+2, num_cols)):
            for ny in range(max(0, y - 1), min(y + 2, num_rows)):
                yield (nx, ny)
            
    
    wordlist = (' '.join(sorted(set(word for (word, path) in solve()))))
    
    stdscr = curses.initscr()
    
    guess = ""
    guessed = []   
    compChoice = ""
    compguessed = []     
    points = 0
    compPoints = 0
    
    stdscr.addstr(0, 0, "Enter 'b' to begin: " +
        "(Ctrl + C will end the application)")
    
    while True:
        c = stdscr.getch()
        if c == ord('b'):
            stuff()
            stdscr.refresh()
            break
        elif c == ord('q'):
            return
        elif c == curses.KEY_HOME:
            x = y = 0
        else:
            y, x = stdscr.getyx()
            stdscr.addstr(0, x, "Incorrect")
            stdscr.move(0, x)
    #error with qu not being treated as one word

    final = []
    check_list = []    

    number = 0
    for item in letter:
        if item == 'q':
            item = 'qu'
        number += 1
        final.append(item + " ")
        check_list.append(item)
        if number % 4 == 0:
            check_list.append('\n')
            final_list = ''.join(final)
            stdscr.addstr(i + 2, 2, final_list)
            stdscr.refresh()
            i += 1
            final = []
    i += 4
    stdscr.addstr(i, 0, wordlist)
    stdscr.refresh()
    i += 10
    
    wordlist = wordlist.split(' ')

    stdscr.addstr(i, 0, "Enter a word:")
    i += 1
    stdscr.move(i, 0)    
    stdscr.refresh()
    
    t_end = time.time() + 10
    comp_time = time.time() + 7
    
    while time.time() < t_end and wordlist:
        stdscr.nodelay(True)        
        char = stdscr.getch()
        stdscr.refresh()
        
        if char != -1:
            if chr(char) == "\n":
                stdscr.addstr(i, 0, " " * len(guess))
                stdscr.move(i, 0)
                if guess in wordlist:
                    wordlist.remove(guess)
                    wordlen = len(guess)
                    
                    if wordlen <= 4:
                        points += 1
                    elif wordlen == 5:
                        points += 2
                    elif wordlen == 6:
                        points += 3
                    elif wordlen == 7:
                        points += 5
                    else:
                        points += 11
                            
                    guessed.append(guess)
                    guess = ""
                else:
                    guess = ""
            # magic number for backspace because i do not 
            # know how to type the char version of it
            elif char == 263:
                if guess:
                    guess = guess[:-1]
                    (y, x) = stdscr.getyx()
                    stdscr.addstr(y, x-1, " ")
                    stdscr.move(y, x-1)
                    stdscr.refresh()
            else:
                guess += str(chr(char))
                
            stdscr.addstr(i, 0, guess)
            
            if comp_time < time.time():
                stdscr.addstr(i+2, 0, "Computer guessed: ")
                compChoice = random.choice(wordlist)
                wordlist.remove(compChoice)
                compguessed.append(compChoice)
                stdscr.addstr(i+3, 0, " " * len(compChoice))
                stdscr.addstr(i+3, 0, compChoice)
                compLen = len(compChoice)
                if compLen <= 4:
                    compPoints += 1
                elif compLen == 5:
                    compPoints += 2
                elif compLen == 6:
                    compPoints += 3
                elif compLen == 7:
                    compPoints += 5
                else:
                    compPoints += 11
                    
                compChoice = ""
                comp_time = time.time() + 7           
                
            
    stdscr.refresh()
    curses.endwin()
    print()    
    print("You guessed: " + ' '.join(guessed))
    print("You recieved", points ,"points")
    print("Computer guessed: " + ' '.join(compguessed))
    print("Comp recieved", compPoints ,"points")
    
        
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print('\nInterrupted...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
