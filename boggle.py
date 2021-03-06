#! /usr/bin/env python3

import time
import random
import sys
import os
import boggle_classes as bc

import curses
from itertools import permutations

random.seed(time.time())

# might be bad to have these global but i need them seen
# throughout the program
player = bc.Player()
comp = bc.Player()
game_board = bc.GameBoard()

# code for my box setup around my graph words
def stuff():
    begin_x = 1
    begin_y = 2
    height = 6
    width = 15
    box1 = curses.newwin(height, width, begin_y, begin_x)
    box1.box()
    box1.refresh()
 
# function that takes care of all the computer actions    
def comp_func(comp, game_board, stdscr, comp_time, i):
    compChoice = ""
    stdscr.addstr(i+2, 0, "Computer guessed: ")
    compChoice = random.choice(game_board._wordlist)
    game_board._wordlist.remove(compChoice)
    comp._guessed.append(compChoice)
    comp.point(compChoice)
    stdscr.addstr(i+3, 0, " " * (len(compChoice) + 10))
    stdscr.addstr(i+3, 0, compChoice)
    compChoice = ""

def main(stdscr):
    number = 1
    i = 1
    arg = 7
    # check for command line arguments involving computer time
    if len(sys.argv) == 2:
        try:
            arg = int(sys.argv[1])
            string = "Computer guess time is " + str(arg)
            stdscr.addstr(i, 0, string)
        except ValueError:
            stdscr.addstr(i, 0, "Computer guess time defaulted to 7")
    elif len(sys.argv) > 2:
        return(2)
   
    i+=1
    
    game_board.generate_graph(number)
    game_board.row_col()
    
    game_board.get_words()
    game_board.get_prefix()
    game_board. assemble_wordlist()
    
    stdscr = curses.initscr()
    
    guess = "" 
    
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
    
    i = game_board.print_graph(i, stdscr)
    
    game_board._wordlist = game_board._wordlist.split(' ')

    stdscr.addstr(i, 0, "Enter a word:")
    i += 1
    stdscr.move(i, 0)    
    stdscr.refresh()
    
    t_end = time.time() + 180
    comp_time = time.time() + arg
    
    while time.time() < t_end and game_board._wordlist:
        stdscr.nodelay(True)
        curses.noecho()
        char = stdscr.getch()
        stdscr.refresh() 
        
        if comp_time < time.time():
            comp_func(comp, game_board, stdscr, comp_time, i)
            comp_time = comp_time + arg             
        
        # this section takes care of user input with getch()
        if char != -1:
            if chr(char) == "\n":
                stdscr.addstr(i, 0, " " * 30)
                stdscr.addstr(i+1, 0, " " * 49)
                stdscr.move(i, 0)
                if guess in game_board._wordlist:
                    game_board._wordlist.remove(guess)
                    player._guessed.append(guess)
                    player.point(guess)
                else:
                    stdscr.addstr(i+1, 0, "That word has "
                    + "either been guessed or isnt correct")
                    
                guess = ""
            # backspace character        
            elif char == 263 or char == 127:
                if guess:
                    guess = guess[:-1]
                    (y, x) = stdscr.getyx()
                    stdscr.addstr(y, x-1, " ")
                    stdscr.move(y, x-1)
                    stdscr.refresh()
                stdscr.addstr(i, 0, " " * 30)
            else:
                if len(guess) > 17:
                    continue
                else:
                    guess += str(chr(char))

            stdscr.addstr(i, 0, guess)
    stdscr.refresh()
    curses.endwin() 

if __name__ == "__main__":
    try:
		# makes sense version is 3 or greater
        if sys.version_info < (3,0,0):
            sys.stderr.write("You need python 3 or higher to run this script\n")
            exit(1)
        os.system('clear')
        os.environ['TERM'] = 'xterm'
        if curses.wrapper(main) == 2:
            print("Too many arguments given")
        else:
            print("You guessed: " + ' '.join(player._guessed))
            print("You recieved", player._score ,"points")
            print("Computer guessed: " + ' '.join(comp._guessed))
            print("Comp recieved", comp._score ,"points")
            print("Full wordlist: ")
            print(game_board._full_wordlist)
    except KeyboardInterrupt:
        print('Interrupted...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
