import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Visualiser")

AQUA = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Block:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row*width
		self.y = col*width
		self.color = WHITE
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == AQUA

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = AQUA

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self,win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self. width))

	def update_neighbours(self, grid):
		self.neighbours = []
		if self.row > 0 and not grid[self.row -1][self.col].is_barrier():
			self.neighbours.append(grid[self.row -1][self.col])

		if self.row < self.total_rows-1 and not grid[self.row +1][self.col].is_barrier():
			self.neighbours.append(grid[self.row +1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def hueristic_dis(cube1, cube2):
	x1, y1 = cube1
	x2, y2 = cube2
	return abs(x1 - x2) + abs(y1 - y2)

def draw_path(came_from, curr_block, draw):
	while curr_block in came_from:
		curr_block = came_from[curr_block]
		curr_block.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {block: float("inf") for row in grid for block in row}
	g_score[start] = 0
	f_score = {block: float("inf") for row in grid for block in row}
	f_score[start] = hueristic_dis(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		curr_block = open_set.get()[2]
		open_set_hash.remove(curr_block)

		if curr_block == end:
			draw_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbour in curr_block.neighbours:
			temp_score = g_score[curr_block] + 1

			if temp_score < g_score[neighbour]:
				came_from[neighbour] = curr_block
				g_score[neighbour] = temp_score
				f_score[neighbour] = temp_score + hueristic_dis(neighbour.get_pos(), end.get_pos())
				if neighbour not in open_set_hash:
					count = count + 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()
		draw()

		if curr_block != start:
			curr_block.make_closed()

	return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			block = Block(i,j,gap,rows)
			grid[i].append(block)

	return grid

def draw_grid(win, rows, width):
	gap = width//rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
	for i in range(rows):
		pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for block in row:
			block.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos,rows, width):
	gap = width//rows
	y,x = pos

	row = y//gap
	col = x//gap

	return row,col




def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				block = grid[row][col]
				if not start and block !=  end:
					start = block
					start.make_start()

				elif not end and block != start:
					end = block
					block.make_end()

				elif block != end and  block != start:
					block.make_barrier()

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos,ROWS,width)
				block = grid[row][col]
				block.reset()
				if block == start:
					start = None
				elif block == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for block in row:
							block.update_neighbours(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
	pygame.quit()

main(WIN,WIDTH)