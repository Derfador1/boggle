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

def box(stdscr, i):
	begin_x = 0
	begin_y = 0
	i = begin_y
	height = 6
	width = 7
	box1 = curses.newwin(height, width, begin_y, begin_x)
	box1.box()
	stdscr.refresh()
	box1.refresh()

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
	i = 0
	
	text = open("/usr/share/dict/british-english", 'r').readlines()
	
	graph = ""
	
	for item in letter:
		graph += str(item).lower()
		if number % 4 == 0:
			graph += ' '
		number += 1
	graph = graph.split()
	#print(graph)
	
	num_rows = len(graph)
	num_cols = len(graph[0])
	
	print(num_rows)
	print(num_cols)
	
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
				print(nx)
				print(ny)
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
	
	stdscr = curses.initscr()
	
	guess = ""
	guessed = []	
	points = 0
	
	stdscr.addstr(0, 0, "Enter 'b' to begin: (Ctrl + C will end the application)")
	
	while True:
		c = stdscr.getch()
		if c == ord('b'):
			print("beginning..")
			box(stdscr, i)
			break
		elif c == ord('q'):
			return
		elif c == curses.KEY_HOME:
			x = y = 0
		else:
			y, x = stdscr.getyx()
			stdscr.addstr(0, x, "Incorrect")
			stdscr.move(0, x)
	

	final = []
	check_list = []	

	number = 0
	for item in letter:
		number += 1
		final.append(item)
		check_list.append(item)
		if number % 4 == 0:
			check_list.append('\n')
			final_list = ''.join(final)
			stdscr.addstr(i + 2, 1, final_list)
			stdscr.refresh()
			i += 1
			final = []
	i += 3
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
			elif char == 263: #magic number for backspace because i do not know how to type the char version of it
				if guess:
					guess = guess[:-1]
					(y, x) = stdscr.getyx()
					stdscr.addstr(y, x-1, " ")
					stdscr.move(y, x-1)
					stdscr.refresh()
			else:
				guess += str(chr(char))
				
			stdscr.addstr(i, 0, guess)
	stdscr.refresh()
	curses.endwin()	
	print("You guessed: " + ' '.join(guessed))
	print("You recieved", points ,"points")
	
		
if __name__ == "__main__":
	try:
		curses.wrapper(main)
	except KeyboardInterrupt:
		print('\nInterrupted...')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
