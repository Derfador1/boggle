#! /usr/bin/env python3

import time
import random
import sys

import curses
from curses.textpad import Textbox, rectangle

random.seed(time.time())


def create_graph(choices, graph_num):
	number = 0
	for key, value in choices.items():
		if number < 4:
			#print(key)
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
	graph1 = []
	graph2 = []
	graph3 = []
	graph4 = []
	graph = []
	
	while True:
		stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

		c = stdscr.getch()
		if c == ord('p'):
			print('Beginning...')
			graph_make(graph1, graph2, graph3, graph4, graph)
			for r in graph:
				for item in r:
					sys.stdout.write(item)
				print()
		elif c == ord('q'):
			break	
		elif c == curses.KEY_HOME:
			x = y = 0
curses.wrapper(main)

#while True:
	#graph_make(graph1, graph2, graph3, graph4, graph)
	#break

#for r in graph:
	#for item in r:
		#sys.stdout.write(item)
	#print()
