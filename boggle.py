#! /usr/bin/env python3

import time
import random
import sys
import os
import boggle_classes as bc

import curses
from itertools import permutations
import re

random.seed(time.time())

def stuff():
    begin_x = 1
    begin_y = 1
    height = 6
    width = 11
    box1 = curses.newwin(height, width, begin_y, begin_x)
    box1.box()
    box1.refresh()
    
def print_graph(i, game_board, stdscr):    
    final = []
    check_list = []    

    number = 0
    for item in game_board._letter:
        if item == 'q':
            item = 'qu'
        number += 1
        final.append(item + " ")
        check_list.append(item)
        if number % 4 == 0:
            check_list.append('\n')
            final_list = ''.join(final)
            stdscr.addstr(i + 1, 2, final_list)
            stdscr.refresh()
            i += 1
            final = []
    i += 4
    stdscr.addstr(i, 0, game_board._wordlist)
    stdscr.refresh()
    i += 10
    return(i)

def main(stdscr):
    # found the following code with a little seperate implementation on:
    # stackoverflow.com/questions/746082/
    # how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-
    # solver#750012
    
    player = bc.Player()
    comp = bc.Player()
    
    game_board = bc.GameBoard()
    
    number = 1
    i = 1
    
    game_board.generate_graph(number)
    game_board.row_col()
    
    alphabet = ''.join(set(''.join(game_board._graph)))
    if 'q' in alphabet:
        alphabet += 'u'
    words = re.compile('[' + alphabet + ']{3,}$', re.I).match
    
    possible_words = set(word.rstrip('\n') 
        for word in open('/usr/share/dict/words') if words(word.lower()))
    prefixes = set(word[:i] 
        for word in possible_words for i in range(2, len(word) + 1))
    
    def solve():
        for y, row in enumerate(game_board._graph):
            for x, letter in enumerate(row):
                #if letter == 'q':
                #    letter = 'qu'
                for result in extending(letter, ((x, y),)):
                    yield result
        
    def extending(prefix, path):
        if prefix in possible_words:
            yield (prefix, path)
        for (nx, ny) in neighbors(path[-1]):
            if (nx, ny) not in path:
                if game_board._graph[ny][nx] == 'q':
                    prefix1 = prefix + 'qu'
                else:
                    prefix1 = prefix + game_board._graph[ny][nx]
                if prefix1 in prefixes:
                    for result in extending(prefix1, path + ((nx, ny),)):
                        yield result
    
    def neighbors(variable):
        x, y = variable
        for nx in range(max(0, x - 1), min(x+2, game_board._num_cols)):
            for ny in range(max(0, y - 1), min(y + 2, game_board._num_rows)):
                yield (nx, ny)
            
    
    game_board._wordlist = (' '.join(sorted(set(word for (word, path) in solve()))))
    
    stdscr = curses.initscr()
    
    guess = "" 
    compChoice = ""
    
    stdscr.addstr(0, 0, "Enter 'b' to begin: " +
        "(Ctrl + C or 'q' will end the application)")
    
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
    
    i = print_graph(i, game_board, stdscr)
    
    game_board._wordlist = game_board._wordlist.split(' ')

    stdscr.addstr(i, 0, "Enter a word:")
    i += 1
    stdscr.move(i, 0)    
    stdscr.refresh()
    
    t_end = time.time() + 20
    comp_time = time.time() + 7
    
    while time.time() < t_end and game_board._wordlist:
        stdscr.nodelay(True)        
        char = stdscr.getch()
        stdscr.refresh()
        
        if char != -1:
            if chr(char) == "\n":
                stdscr.addstr(i, 0, " " * len(guess))
                stdscr.move(i, 0)
                if guess in game_board._wordlist:
                    game_board._wordlist.remove(guess)
                    player._guessed.append(guess)
                    player.point(guess)
                    guess = ""
                else:
                    guess = ""
            # captures the backspace character
            elif char == curses.KEY_BACKSPACE:
                if guess:
                    guess = guess[:-1]
                    (y, x) = stdscr.getyx()
                    stdscr.addstr(y, x-1, " ")
                    stdscr.move(y, x-1)
                    stdscr.refresh()
            else:
                if len(guess) > 17: #changed this
                    continue
                else:
                    guess += str(chr(char))

            stdscr.addstr(i, 0, guess)
            
            if comp_time < time.time():
                stdscr.addstr(i+2, 0, "Computer guessed: ")
                compChoice = random.choice(game_board._wordlist)
                game_board._wordlist.remove(compChoice)
                comp._guessed.append(compChoice)
                comp.point(compChoice)
                stdscr.addstr(i+3, 0, " " * len(compChoice))
                stdscr.addstr(i+3, 0, compChoice)
                compChoice = ""
                comp_time = time.time() + 7                 
            
    stdscr.refresh()
    curses.endwin()
    print()    
    print("You guessed: " + ' '.join(player._guessed))
    print("You recieved", player._score ,"points")
    print("Computer guessed: " + ' '.join(comp._guessed))
    print("Comp recieved", comp._score ,"points")
    
        
if __name__ == "__main__":
    try:
        os.system('clear')
        curses.wrapper(main)
    except KeyboardInterrupt:
        print('\nInterrupted...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
