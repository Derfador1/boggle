#! /usr/bin/env python3

import time
import random
import sys
import os

import curses
from curses.textpad import Textbox, rectangle
from itertools import permutations
import re

random.seed(time.time())

#acquired from stackoverflow.com/questions/21784625/how-to-input-a-word-in-ncurses-screen
def my_raw_input(stdscr, r, c, prompt_string):
	curses.echo()
	stdscr.addstr(r, c, prompt_string)
	stdscr.refresh()
	input = stdscr.getstr(r + 1, c, 20)
	return input


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
die15 = ['n', 'u', 'i', 'h', 'm', 'Qu']


choices = {
		'zero':die0, 'one':die1, 'two':die2, 'three':die3, 
		'four':die4, 'five':die5, 'six':die6, 'seven':die7, 'eight':die8, 
		'nine':die9, 'ten':die10, 'eleven':die11, 'twelve':die12, 'thirteen':die13, 
		'fourteen':die14, 'fifteen':die15
		}

def main(stdscr):
	# found the following code with a little seperate implementation on:
	# stackoverflow.com/questions/746082/
	# how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver#750012
	
	letter = [random.choice(i) for i in choices.values()]
	number = 1
	
	text = open("/usr/share/dict/british-english", 'r').readlines()
	
	graph = ""
	
	for item in letter:
		graph += str(item).lower()
		if number % 4 == 0:
			graph += ' '
		number += 1
	graph = graph.split()
	print(graph)
	
	num_rows = len(graph)
	num_cols = len(graph[0])
	
	alphabet = ''.join(set(''.join(graph)))
	words = re.compile('[' + alphabet + ']{3,}$', re.I).match
	
	possible_words = set(word.rstrip('\n') for word in open('/usr/share/dict/words') if words(word.lower()))
	prefixes = set(word[:i] for word in possible_words for i in range(2, len(word) + 1))
	
	def solve():
		for y, row in enumerate(graph):
			for x, letter in enumerate(row):
				for result in extending(letter, ((x, y),)):
					yield result
		
	def extending(prefix, path):
		if prefix in possible_words:
			yield (prefix, path)
		for (nx, ny) in neighbors(path[-1]):
			if (nx, ny) not in path:
				prefix1 = prefix + graph[ny][nx]
				if prefix1 in prefixes:
					for result in extending(prefix1, path + ((nx, ny),)):
						yield result
	
	def neighbors(variable):
		(x, y) = variable
		for nx in range(max(0, x - 1), min(x+2, num_cols)):
			for ny in range(max(0, y - 1), min(y + 2, num_rows)):
				yield (nx, ny)
			
	
	wordlist = (' '.join(sorted(set(word for (word, path) in solve()))))
	
	while True:
		stdscr = curses.initscr()

		stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
		
		final = []
		check_list = []
		
		c = stdscr.getch()
		if c == ord('b'):
			begin_x = 0
			begin_y = 0
			height = 6
			width = 7
			print('Beginning...')
			box1 = curses.newwin(height, width, begin_y, begin_x)
			box1.box()
			stdscr.refresh()
			box1.refresh()
			number = 0
			i = 1
			for item in letter:
				number += 1
				final.append(item)
				check_list.append(item)
				if number % 4 == 0:
					check_list.append('\n')
					final_list = ''.join(final)
					stdscr.addstr(i+1, 1, final_list)
					stdscr.refresh()
					i += 1
					final = []
			i += 2
			stdscr.addstr(i, 0, wordlist)
			stdscr.refresh()
			
			guess = ""
			guessedWords = []
			
			i += 10
			
			wordlist = wordlist.split(' ')
			
			points = 0
			
			t_end = time.time() + 1
			
			while time.time() < t_end:
				choice = (my_raw_input(stdscr, i, 0, "Make a guess: ").lower().decode(encoding='utf-8'))
				stdscr.nodelay(True)
				stdscr.refresh()
				stdscr.getch()
				curses.endwin()
		
				#if str(choice) in correct_words:
			
			#raw_input change
			
			##decode(encoding='utf-8')
			
			#curses.echo()
			
			#while wordlist:
				#stdscr.nodelay(True)
				#s = stdscr.getch()
				#if s != -1:
					#chr(s)
					#if s == 10:
						#for x in range(0, len(guess)):
							#stdscr.addstr(" ")
						#stdscr.move(i+1, 0)
						#if guess in wordlist:
							#wordlist.remove(guess)
							#wordlen = len(guess)
							#if wordlen <= 4:
								#points += 1
							
							#guessedWords.append(guess)
							#guess = ""
						#else:
							#guess = ""
					#elif s == 263:
						#if guess:
							#guess = guess.replace(guess[-1],"")
						#else:
							#pass
					#elif s < 256:
						#guess += str(chr(s))
				
			#stdscr.nodelay(False)
			#stdscr.addstr(guess + "\n")
			#stdscr.addstr(' '.join(wordlist))
			#stdscr.addstr("\nYou correctly guessed:\n")
			#stdscr.getkey()
		elif c == ord('q'):
			break	
		elif c == curses.KEY_HOME:
			x = y = 0	
	
		
if __name__ == "__main__":
	try:
		curses.wrapper(main)
	except KeyboardInterrupt:
		print('\nInterrupted...')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
