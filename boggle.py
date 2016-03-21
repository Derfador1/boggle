#! /usr/bin/env python3

import time
import random

die0 = ['R', 'I', 'F', 'O', 'B', 'X']
die1 = ['I', 'F', 'E', 'H', 'E', 'Y']
die2 = ['D', 'E', 'N', 'O', 'W', 'S']
die3 = ['U', 'T', 'O', 'K', 'N', 'D']
die4 = ['H', 'M', 'S', 'R', 'A', 'O']
die5 = ['L', 'U', 'P', 'E', 'T', 'S']
die6 = ['A', 'C', 'I', 'T', 'O', 'A']
die7 = ['Y', 'L', 'G', 'K', 'U', 'E']
die8 = ['Qu', 'B', 'M', 'J', 'O', 'A']
die9 = ['E', 'H', 'I', 'S', 'P', 'N']
die10 = ['V', 'E', 'T', 'I', 'G', 'N']
die11 = ['B', 'A', 'L', 'I', 'Y', 'T']
die12 = ['E', 'Z', 'A', 'V', 'N', 'D']
die13 = ['R', 'A', 'L', 'E', 'S', 'C']
die14 = ['U', 'W', 'I', 'L', 'R', 'G']
die15 = ['P', 'A', 'C', 'E', 'M', 'D']


choices = {
		'zero':die0, 'one':die1, 'two':die2, 'three':die3, 
		'four':die4, 'five':die5, 'six':die6, 'seven':die7, 'eight':die8, 
		'nine':die9, 'ten':die10, 'eleven':die11, 'twelve':die12, 'thirteen':die13, 
		'fourteen':die14, 'fifteen':die15
		}


for key, value in choices.items():
	print(random.choice(value), key)
