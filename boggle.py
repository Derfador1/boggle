#! /usr/bin/env python3

import time
import random
import sys

import curses
from curses.textpad import Textbox, rectangle
from itertools import permutations
import re

random.seed(time.time())


def create_graph(choices, graph_num):
	number = 0
	for key, value in choices.items():
		if number < 4:
			stuff = random.choice(value)
			number += 1
			graph_num.append(stuff)
			
def graph_make(graph1, graph2, graph3, graph4, graph):
	create_graph(choices, graph1)
	graph.append(graph1)
	create_graph(choices, graph2)
	graph.append(graph2)
	create_graph(choices, graph3)
	graph.append(graph3)
	create_graph(choices, graph4)
	graph.append(graph4)

#q is qu
#die0 = ['a', 'a', 'a', 'f', 'r', 's']
#die1 = ['a', 'a', 'e', 'e', 'e', 'e']
#die2 = ['a', 'a', 'f', 'i', 'r', 's']
#die3 = ['a', 'd', 'e', 'n', 'n', 'n']
#die4 = ['a', 'e', 'e', 'e', 'e', 'm']
#die5 = ['a', 'e', 'e', 'g', 'm', 'u']
#die6 = ['a', 'e', 'g', 'm', 'n', 'n']
#die7 = ['a', 'f', 'i', 'r', 's', 'y']
#die8 = ['q', 'b', 'm', 'j', 'o', 'a']
#die9 = ['b', 'j', 'k', 'q', 'x', 'z']
#die10 = ['c', 'c', 'e', 'n', 's', 't']
#die11 = ['c', 'e', 'i', 'i', 'l', 't']
#die12 = ['c', 'e', 'i', 'p', 'l', 't']
#die13 = ['c', 'e', 'i', 'p', 's', 't']
#die14 = ['d', 'd', 'h', 'n', 'o', 't']
#die15 = ['d', 'h', 'h', 'l', 'o', 'r']
#die16 = ['d', 'h', 'l', 'n', 'o', 'r']
#die17 = ['e', 'i', 'i', 'i', 't', 't']
#die18 = ['e', 'm', 'o', 't', 't', 't']
#die19 = ['e', 'n', 's', 's', 's', 'u']
#die20 = ['f', 'i', 'p', 'r', 's', 'y']
#die21 = ['g', 'o', 'r', 'r', 'v', 'w']
#die22 = ['i', 'p', 'r', 'r', 'r', 'y']
#die23 = ['n', 'o', 'o', 't', 'u', 'w']
#die24 = ['o', 'o', 'o', 't', 't', 'u']

#choices = {
		#'zero':die0, 'one':die1, 'two':die2, 'three':die3, 
		#'four':die4, 'five':die5, 'six':die6, 'seven':die7, 'eight':die8, 
		#'nine':die9, 'ten':die10, 'eleven':die11, 'twelve':die12, 'thirteen':die13, 
		#'fourteen':die14, 'fifteen':die15, 'sixteen':die16, 'seventeen':die17, 'eighteen':die18,
		#'nineteen':die19,'twenty':die20, 'twenty-one':die21, 'twenty-two':die22, 'twenty-three':die23,
		#'twenty-four':die24
		#}
		
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
		stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
		final = []
		tmp = []
		win = curses.initscr()
		c = stdscr.getch()
		if c == ord('b'):
			begin_x = 0
			begin_y = 0
			height = 6
			width = 7
			print('Beginning...')
			box1 = curses.newwin(height, width, begin_y, begin_x)
			box1.box()
			win.refresh()
			box1.refresh()
			number = 0
			i = 1
			for item in letter:
				number += 1
				final.append(item)
				tmp.append(item)
				if number % 4 == 0:
					tmp.append('\n')
					final_list = ''.join(final)
					stdscr.addstr(i+1, 1, final_list)
					win.refresh()
					i += 1
					final = []
			#final1 = ''.join(final)
			
			#stdscr.addstr(i, 2, final1)
			#win.refresh()
			stdscr.addstr(i+2, 0, wordlist)
			win.refresh()
			stdscr.addstr(i+4, 0, wordlist[2])
			win.refresh()
			
			wordlist = wordlist.split(' ')
			for item in wordlist:
				print(item)

			#stuff = 0
			#for item in tmp:
				#stuff += 1
				#if number % 4 == 0: 
					#print(item)
			
			#win.getch()
		elif c == ord('q'):
			break	
		elif c == curses.KEY_HOME:
			x = y = 0	
	
		
if __name__ == "__main__":
	try:
		curses.wrapper(main)
	#catches the keyboard interrupt if ^C is used to end program
	except KeyboardInterrupt:
		print('\nInterrupted...')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

#def main(stdscr):
	#graph1 = []
	#graph2 = []
	#graph3 = []
	#graph4 = []
	#graph = []
	
	#while True:
		#stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

		#c = stdscr.getch()
		#if c == ord('p'):
			#print('Beginning...')
			#graph_make(graph1, graph2, graph3, graph4, graph)
			#for r in graph:
				#for item in r:
					#sys.stdout.write(item)
				#print()
		#elif c == ord('q'):
			#break	
		#elif c == curses.KEY_HOME:
			#x = y = 0
#curses.wrapper(main)
