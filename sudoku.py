import requests
import numpy
import pygame
import sys
from tkinter import *
from tkinter import messagebox

OFFSET = 50
# Square size
SS = 50
# Board size
SIZE = SS*9 + OFFSET
BLACK = (0,0,0)
WHITE = (255,255,255)
OFFWHITE = (245,245,245)
GREY = (220,220,220)
INPUTS = {pygame.K_0:0,
		  pygame.K_1:1,
		  pygame.K_2:2,
		  pygame.K_3:3,
		  pygame.K_4:4,
		  pygame.K_5:5,
		  pygame.K_6:6,
		  pygame.K_7:7,
		  pygame.K_8:8,
		  pygame.K_9:9}


class Grid():
	def __init__(self, game, display):
		self.game = game
		self.display = display
		self.chosen = None
		grid = [[0]*9 for x in range(9)]
		for row in range(9):
			for col in range(9):
				if self.game.grid[row][col] == 0:
					playable = True
				else:
					playable = False
				grid[row][col] = {'x':OFFSET+row*SS,
								  'y':OFFSET+col*SS,
								  'row':row,
								  'col':col,
								  'rect':pygame.Rect(OFFSET+row*SS,OFFSET+col*SS,SS,SS),
								  'num':self.game.grid[row][col],
								  'playable':playable}
		self.grid = grid


	def render(self):
		# Draw border lines
		font = pygame.font.SysFont('comicsansms',34)
		pygame.draw.line(self.display, BLACK, (OFFSET,OFFSET),(OFFSET,SIZE),4)
		pygame.draw.line(self.display, BLACK, (OFFSET,OFFSET),(SIZE,OFFSET),4)
		pygame.draw.line(self.display, BLACK, (SIZE,OFFSET),(SIZE,SIZE),4)
		pygame.draw.line(self.display, BLACK, (OFFSET,SIZE),(SIZE,SIZE),4)
		for row in range(9):
			for col in range(9):
				if self.grid[row][col] == self.chosen:
					color = GREY
				elif self.grid[row][col]['playable'] == True:
					color = WHITE
				else:
					color = OFFWHITE
				pygame.draw.rect(self.display, color, self.grid[row][col]['rect'])
				if self.grid[row][col]['num']!=0:
					number = str(self.grid[row][col]['num']).split('.')[0]
					text = font.render(number,False,BLACK)
					self.display.blit(text,(self.grid[row][col]['x']+20,self.grid[row][col]['y']+20))
		for i in range(8):
			x = SS*i+SS+OFFSET
			if (i+1)%3 == 0:
				thickness = 3
			else:
				thickness = 1
			pygame.draw.line(self.display, BLACK,(x,OFFSET),(x,SIZE), thickness)
			pygame.draw.line(self.display, BLACK,(OFFSET,x),(SIZE,x), thickness)


	def handle_click(self, pos):
		for row in range(9):
			for col in range(9):
				if self.grid[row][col]['rect'].collidepoint(pos) and self.grid[row][col]['playable'] == True:
					self.chosen = self.grid[row][col]
		print(self.chosen)


	def handle_num(self, number):
		print(number)
		if self.chosen:
			self.chosen['num'] = number
			row = self.chosen['row']
			col = self.chosen['col']
			self.game.grid[row][col] = number


	def check_win(self):
		if numpy.array_equal(self.game.grid,self.game.solution):
			print('SUCCESS!')



class Sudoku():
	def __init__(self):
		'''
		Initialize grid
		'''
		data = requests.get('http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=1').json()
		grid = numpy.zeros((9,9))
		for number in data['squares']:
			grid[number['x']][number['y']] = number['value']
		print(grid)
		self.grid = grid
		self.solution = self.grid


	def check(self, row, col, number):
		# Check row
		for i in range(9):
			if self.grid[row][i] == number:
				return False
		# Check col
		for i in range(9):
			if self.grid[i][col] == number:
				return False
		# Check square
		corner_r = (row//3)*3
		corner_c = (col//3)*3
		for i in range(corner_r, corner_r+3):
			for j in range(corner_c, corner_c+3):
				if self.grid[i][j] == number:
					return False
		return True


	def solve(self):
		for row in range(9):
			for col in range(9):
				if self.solution[row][col] == 0:
					for i in range(1,10):
						if self.check(row,col,i):
							self.solution[row][col] = i
							self.solve()
							self.solution[row][col] = 0
					return
		print(self.solution)
		return self.solution


def main():
	RUNNING = True
	pygame.init()
	game = Sudoku()
	#game.solve()
	display = pygame.display.set_mode((1500,1500),0,32)
	grid = Grid(game, display)
	while RUNNING:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUNNING = False
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				print(pos)
				grid.handle_click(pos)
			if event.type == pygame.KEYDOWN:
				if event.key in INPUTS.keys():
					grid.handle_num(INPUTS[event.key])

		display.fill((255,255,255))
		grid.render()
		pygame.display.update()
		grid.check_win()
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()

