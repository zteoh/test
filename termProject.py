from tkinter import *
import random
import csv
from tkinter import filedialog
from pygame import mixer, font


##############################################################################
#initialisation#
##############################################################################

def init(data):

	data.mode = "splashScreen"

	#board
	data.board = []
	data.rows = 15
	data.cols = 20
	data.margin = 30

	#game
	data.gameOver = False
	data.nextLevel = False
	data.paused = False
	data.debugMode = False
	data.showMode = False
	data.score = 0
	data.lives = 5

	#objects in class
	data.shepherd = Shepherd(data)
	data.wolf = Wolf(data)
	data.hedges = Hedges(data)
	data.portals = Portals(data)
	data.safeZoneHedge = SafeZoneHedge(data)
	data.sheep = Sheep(data)
	data.safeZoneEntry = SafeZoneEntry(data)
	data.safeZone = SafeZone(data)

	data.noSheeps = 5
	data.sheepsPos = dict() 
	data.sheepsDir = dict()
	for sheep in range(data.noSheeps):
		data.sheepsDir[sheep] = (0,0)

	#i have to keep this at the end because it uses the values in data
	loadBoard(data, fileName = "Levels/HerderLevel1.csv")

	data.sheepCounter = 0
	data.wolfCounter = 0

	#generator_board
	data.generator_rows = 15
	data.generator_cols = 20 
	data.margin = 30
	data.generator_board = [([0] * data.generator_cols) for row in range(data.generator_rows)]

	#generator_board objects
	data.hedges = Landscape(-2)
	data.erase = Landscape(0)
	data.portals = Landscape(0)
	data.safeZoneEntry = Landscape(-1)
	data.safeZone = Landscape(-5)
	data.safeZoneHedge = Landscape(-2)

	#generator_board modes
	data.checkMode = False
	data.hedgeMode = False
	data.eraseMode = False
	data.portalsMode = False
	data.safeZoneMode = False
	data.safeZoneEntryMode = False
	data.safeZoneHedgeMode = False

	data.instructionMode = True

	####################################

	data.sheepPic = PhotoImage(file = "graphics/sheep55.gif")
	data.sheepPicR = PhotoImage(file = "graphics/sheep55R.gif")
	data.sheepPicL = PhotoImage(file = "graphics/sheep55L.gif")
	data.sheepPicB = PhotoImage(file = "graphics/sheep55B.gif")

	data.wolfPic = PhotoImage(file = "graphics/wolf55.gif")
	data.wolfPicR = PhotoImage(file = "graphics/wolf55R.gif")
	data.wolfPicL = PhotoImage(file = "graphics/wolf55L.gif")
	data.wolfPicB = PhotoImage(file = "graphics/wolf55B.gif")

	data.shepherdPic = PhotoImage(file = "graphics/shepherd55.gif")
	data.shepherdPicR = PhotoImage(file = "graphics/shepherd55R.gif")
	data.shepherdPicL = PhotoImage(file = "graphics/shepherd55L.gif")
	data.shepherdPicB = PhotoImage(file = "graphics/shepherd55B.gif")

	data.splashScreen1Pic = PhotoImage(file = "graphics/splashScreenScene1.gif")
	data.splashScreen2Pic = PhotoImage(file = "graphics/splashScreenScene2.gif")
	data.splashScreen3Pic = PhotoImage(file = "graphics/splashScreenScene3.gif")
	data.splashScreen4Pic = PhotoImage(file = "graphics/splashScreenScene4.gif")

	data.grassPic = PhotoImage(file = "graphics/oliveDrab1.2.gif")
	data.entryPic = PhotoImage(file = "graphics/oliveDrab2.gif")
	data.safeZonePic = PhotoImage(file = "graphics/oliveDrab1.1.gif")
	data.hedgePic = PhotoImage(file = "graphics/oliveDrab3.gif")

	##############################################################################

	data.highScoresFile = open("highScores.txt","r+")
	data.highScores = data.highScoresFile.read().split(",")
	data.highScores = sorted(data.highScores,key=int, reverse = True)
	
	##############################################################################

	data.helpTimeCount = 0
	data.sheep120Pic = PhotoImage(file = "graphics/sheep120.gif")
	data.wolf120Pic = PhotoImage(file = "graphics/wolf120.gif")
	data.shepherd120Pic = PhotoImage(file = "graphics/shepherd120.gif")

	data.splashTimerCount = 0

	##############################################################################
	data.mouseOnPlay = False
	data.mouseOnHelp = False
	data.mouseOnDIY = False
	data.mouseOnScore = False

	##############################################################################
	data.gameDifficultyMode = True
	data.difficultyEasy = False
	data.difficultyHard = False
	data.difficultyMulti = False


##############################################################################
# Classes #
##############################################################################
class Shepherd(object):

	def __init__ (self, data, row = None, col = None):
		if row == None or col == None:
			row = random.randrange(data.rows)
			col = random.randrange(data.cols)

		self.row = row
		self.col = col
		self.direction = (0,0)
		self.no = 10

		self.dead = False

	def move(self, event, data):
		self.direction = (0,0)
		if (event.keysym == "Left"):    
			self.direction = (0, -1)
		elif (event.keysym == "Right"): 
			self.direction = (0,  1)
		elif (event.keysym == "Up"):    
			self.direction = (-1, 0) 
		elif (event.keysym == "Down"):  
			self.direction = ( 1, 0)
		
		#original, change, new
		drow, dcol = self.direction
		row, col = self.row, self.col
		newRow, newCol = (row + drow)%data.rows, (col + dcol)%data.cols

		#checks whether there is a sheep there
		if data.board[newRow][newCol] == data.sheep.no:
			data.board[newRow][newCol] = 15
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

			data.shepherd = WithAnimal(data, self.row, self.col)
			sheepsPosList = [pos for pos in data.sheepsPos.values()]
			sheep = sheepsPosList.index((newRow, newCol))
			data.sheepsPos[sheep] = None
		
		#checking if the cell is unoccuppied
		elif data.board[newRow][newCol] == 0 or data.board[newRow][newCol] == data.portals.no:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

	def killed(self):
		self.dead = True

	def revive(self, data):
		self.row = random.randrange(data.rows)
		self.col = random.randrange(data.cols)

		while data.board[self.row][self.col] != 0 \
		or 0 > self.row and self.row >= data.rows and 0 > self.col and self.col >= data.cols:
				self.row = random.randrange(data.rows)
				self.col = random.randrange(data.cols)
			
		data.board[self.row][self.col] = self.no

		data.shepherd.dead = False


	#load is used when placing it on to the board (not drawing)
	def loadShepherd(self, data):
		while data.board[self.row][self.col] != 0 \
			or 0 > self.row and self.row >= data.rows and 0 > self.col and self.col >= data.cols:
					self.row = random.randrange(data.rows)
					self.col = random.randrange(data.cols)
		data.board[self.row][self.col] = self.no

class WithAnimal(Shepherd):
	def __init__(self, data, row, col):
		super().__init__ (data)
		self.no = 15
		self.row = row
		self.col = col

	def move(self, event, data):
		self.direction = (0,0)

		#computer keys to directions
		if (event.keysym == "Left"):    
			self.direction = (0, -1)
		elif (event.keysym == "Right"): 
			self.direction = (0,  1)
		elif (event.keysym == "Up"):    
			self.direction = (-1, 0) 
		elif (event.keysym == "Down"):  
			self.direction = ( 1, 0)

		#original, change, new
		drow, dcol = self.direction
		row, col = self.row, self.col
		newRow, newCol = (row + drow)%data.rows, (col + dcol)%data.cols

		#check for empty cell
		if data.board[newRow][newCol] == 0:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

		#entering safe zone- place sheep 
		if data.board[newRow][newCol] == data.safeZoneEntry.no:
			# data.board[row][col] = data.shepherd.no
			# self.row, self.col = row, col
			data.shepherd = Shepherd(data, self.row, self.col)
			data.board[row][col] = data.shepherd.no
			data.board[newRow + drow][newCol + dcol] = 50
			data.score += 1
			
class Hedges(object):
	def __init__ (self, data):
		self.no = -2

	#load is used when placing it on to the board (not drawing)
	def loadHedges(self, data):
		for row in range(data.rows):
			data.board[row][0] = self.no
			data.board[row][data.cols-1] = self.no
		for col in range(data.cols):
			data.board[0][col] = self.no
			data.board[data.rows-1][col] = self.no

class SafeZoneHedge (object):
	def __init__ (self, data):
		self.colLeft = 3 * data.cols//8
		self.colRight = 5 * data.cols//8
		self.rowTop = 1 * data.rows//3
		self.rowBottom = 2 *data.rows//3
		self.no = -2

	def loadSafeZoneHedge(self, data):
		for row in range(self.rowTop, self.rowBottom+1):
			data.board[row][self.colLeft] = self.no
			data.board[row][self.colRight] = self.no
		for col in range(self.colLeft, self.colRight+1):
			data.board[self.rowTop][col] = self.no
			data.board[self.rowBottom][col] = self.no

class SafeZoneEntry (object):
	def __init__(self, data):
		self.row = data.safeZoneHedge.rowTop + ((data.safeZoneHedge.rowBottom - data.safeZoneHedge.rowTop)//2)
		self.col = data.safeZoneHedge.colLeft + ((data.safeZoneHedge.colRight - data.safeZoneHedge.colLeft)//2)
		self.no = -1

	def loadSafeZoneEntry(self, data):

		data.board[self.row][data.safeZoneHedge.colLeft] = self.no
		data.board[self.row+1][data.safeZoneHedge.colLeft] = self.no

		data.board[self.row][data.safeZoneHedge.colRight] = self.no
		data.board[self.row+1][data.safeZoneHedge.colRight] = self.no

		data.board[data.safeZoneHedge.rowTop][self.col] = self.no
		data.board[data.safeZoneHedge.rowTop][self.col+1] = self.no

		data.board[data.safeZoneHedge.rowBottom][self.col] = self.no
		data.board[data.safeZoneHedge.rowBottom][self.col+1] = self.no

class SafeZone(object):
	def __init__ (self, data):
		self.colLeft = 3 * data.cols//8
		self.colRight = 5 * data.cols//8
		self.rowTop = 1 * data.rows//3
		self.rowBottom = 2 *data.rows//3
		self.no = -5

	def loadSafeZone(self, data):
		for row in range(self.rowTop, self.rowBottom+1):
			for col in range(self.colLeft, self.colRight+1):
				data.board[row][col] = self.no
				data.board[row][col] = self.no

class Portals(object):
	def __init__ (self, data):
		self.row = data.rows//2
		self.col = data.cols//2
		self.no = 0

	def loadPortals(self, data):
		for col in [0, data.cols - 1]:
			for i in range (2):
				data.board[self.row+i][col] = self.no
				data.board[self.row-i][col] = self.no
		for row in [0, data.rows - 1]:
			for i in range (2):
				data.board[row][self.col+i] = self.no
				data.board[row][self.col-i] = self.no

class Sheep(object):
	def __init__ (self, data):
		self.no = 5

		self.row = random.randrange(data.rows)
		self.col = random.randrange(data.cols)

		self.direction = (0,0)

	def move(self, data):
		#to test out sheep movement
		for sheep in range(len(data.sheepsPos)):
			if data.sheepsPos[sheep] != None:
				self.row, self.col = data.sheepsPos[sheep]
				initialDirection = data.sheepsDir[sheep]

				#converting the direction to an index from 0-4
				directions = [  (0,0), (0,1), (0,-1), (1,0), (-1,0)     ]
				initialDirectionIndex = directions.index(initialDirection)

				#if initial dir is (0,0), equal chance for moving on every direction
				dirs = \
				[   [(0,0), (0,0), (0,1), (0,1), (0,-1), (0,-1), (1,0), (1,0), (-1,0), (-1,0)],
					[(0,1), (0,1), (0,1), (0,-1), (0,0), (0,0), (1,0), (1,0), (-1,0), (-1,0)],
					[(0,-1), (0,-1), (0,-1), (0,1), (0,0), (0,0), (1,0), (1,0), (-1,0), (-1,0)],
					[(1,0), (1,0), (1,0), (-1,0), (0,0), (0,0), (0,1), (0,1), (0,-1), (0,-1)],
					[(-1,0), (-1,0), (-1,0), (1,0), (0,0), (0,0), (0,1), (0,1), (0,-1), (0,-1)]     ]


				#convert probability into an integer pointing to a direction
				probability = random.randrange(10)
				self.direction = dirs[initialDirectionIndex][probability]

				drow, dcol = self.direction
				row, col = self.row, self.col
				newRow, newCol = (row + drow)%data.rows, (col + dcol)%data.cols

				#checking if the cell is unoccuppied
				if data.board[newRow][newCol] == 0:
					data.board[newRow][newCol] = self.no
					data.board[row][col] = 0
					self.row, self.col = newRow, newCol
					data.sheepsDir[sheep] = (drow, dcol)
					data.sheepsPos[sheep] = (self.row, self.col)


	def loadSheep(self,data):
		for sheep in range(data.noSheeps):
			while data.board[self.row][self.col] != 0:
				self.row = random.randrange(data.rows)
				self.col = random.randrange(data.cols)


			data.sheepsPos[sheep] = (self.row, self.col)

			data.board[self.row][self.col] = self.no

class Wolf(object):
	def __init__(self, data):
		self.no = -10

		self.row = data.rows//4
		self.col = data.cols//4

		self.direction = (0,0)

	def controlledMove(self, event, data):
		self.direction = (0,0)
		if (event.char == "a"):    
			self.direction = (0, -1)
		elif (event.char == "d"): 
			self.direction = (0,  1)
		elif (event.char == "w"):    
			self.direction = (-1, 0) 
		elif (event.char == "s"):  
			self.direction = ( 1, 0)

		#original, change, new
		drow, dcol = self.direction
		row, col = self.row, self.col
		newRow, newCol = (row + drow)%data.rows, (col + dcol)%data.cols

		#DEVOURS THE SHEEP
		if data.board[newRow][newCol] == 5:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

			sheepsPosList = [pos for pos in data.sheepsPos.values()]

			sheep = sheepsPosList.index((newRow, newCol))
			data.sheepsPos[sheep] = None
			data.lives -= 1

		#DEVOUR THE SHEPHERD
		elif data.board[newRow][newCol] == 10 or\
		data.board[newRow][newCol] == 15:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol
			data.shepherd.killed()
			data.lives -= 1

		#checking if the cell is unoccuppied
		elif data.board[newRow][newCol] == 0:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

	def move(self, data):
		row, col = self.row, self.col
		newRow, newCol = self.row, self.col

		if data.difficultyHard:
			newPath = bfs(data.board, newRow, newCol)

			if len(newPath) == 0:
				pass
			elif len(newPath) > 1:
				newRow, newCol = newPath[1]

		elif data.difficultyEasy:
			#this section seeks to use an easy AI and manhatten distance

			#calculating the distance from the wolf to the sheep
			#and then storing it in a dictionary- sheepsDistance
			#where the key will be the distance, the value will be the sheep's index (sheep)
			row, col = self.row, self.col
			newRow, newCol = self.row, self.col

			sheepsDistance = dict()
			
			for sheep in range(data.noSheeps):
				if data.sheepsPos[sheep] != None:
					sheepRow, sheepCol = data.sheepsPos[sheep]
					wolfRow, wolfCol = self.row, self.col

					distance = abs(sheepCol - wolfCol) + abs(sheepRow - wolfRow)
					# print(sheep, distance)

					sheepsDistance[distance] = sheep

			#find the index of the sheep with the shortest distance
			if len(sheepsDistance) != 0:
				minDistSheepIndex = sheepsDistance.get(min(sheepsDistance))

				minDistSheepPos = data.sheepsPos[minDistSheepIndex]

				minDistSheepMoveX = minDistSheepPos[0] - wolfRow
				minDistSheepMoveY = minDistSheepPos[1] - wolfCol
				minDistSheepMove = (minDistSheepMoveX, minDistSheepMoveY)

				#find out how to move to the closest sheep
				if minDistSheepMoveX != 0:
					if minDistSheepMoveX > 0:
						newRow += 1
						minDistSheepMoveX -= 1
					else:
						newRow -= 1
						minDistSheepMoveX += 1

					#checking for collision
					if data.board[newRow][newCol] == data.hedges.no \
					or data.board[newRow][newCol] == data.safeZoneEntry.no\
					or data.board[newRow][newCol] == data.safeZoneHedge.no:
						newRow, newCol = self.row, self.col
						if minDistSheepMoveY != 0:
							if minDistSheepMoveY > 0:
								newCol += 1
								minDistSheepMoveY -= 1
							else:
								newCol -= 1
								minDistSheepMoveY += 1


				elif minDistSheepMoveY != 0:
					if minDistSheepMoveY > 0:
						newCol += 1
						minDistSheepMoveY -= 1
					else:
						newCol -= 1
						minDistSheepMoveY += 1

					#checking for colision
					if data.board[newRow][newCol] == data.hedges.no \
					or data.board[newRow][newCol] == data.safeZoneEntry.no\
					or data.board[newRow][newCol] == data.safeZoneHedge.no:
						newRow, newCol = self.row, self.col
						if minDistSheepMoveX != 0:
							if minDistSheepMoveX > 0:
								newRow += 1
								minDistSheepMoveX -= 1
							else:
								newRow -= 1
								minDistSheepMoveX += 1


		#DEVOURS THE SHEEP
		if data.board[newRow][newCol] == 5:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

			sheepsPosList = [pos for pos in data.sheepsPos.values()]
			sheep = sheepsPosList.index((newRow, newCol))
			data.sheepsPos[sheep] = None
			data.lives -= 1

		#DEVOUR THE SHEPHERD
		elif data.board[newRow][newCol] == 10 or\
		data.board[newRow][newCol] == 15:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol
			data.shepherd.killed()
			data.lives -= 1

		#checking if the cell is unoccuppied
		elif data.board[newRow][newCol] == 0:
			data.board[newRow][newCol] = self.no
			data.board[row][col] = 0
			self.row, self.col = newRow, newCol

	#load is used when placing it on to the board (not drawing)
	def loadWolf(self, data):
		while data.board[self.row][self.col] != 0 \
			or 0 > self.row and self.row >= data.rows and 0 > self.col and self.col >= data.cols:
					self.row = random.randrange(data.rows)
					self.col = random.randrange(data.cols)
		data.board[self.row][self.col] = self.no

class Landscape(object):
	def __init__ (self, no):
		self.no = no

	def place(self, event, data):
		rowHeight = (data.height - 2 * data.margin)//data.generator_rows
		colWidth = (data.width - 2 * data.margin)//data.generator_cols
		row = (event.y - data.margin)//rowHeight
		col = (event.x - data.margin)//colWidth

		# print (row, col, data.generator_rows, data.generator_cols)
		if (0 <= row and row < data.generator_rows) and (0<= col and col < data.generator_cols):
			data.generator_board[row][col] = self.no

##############################################################################
# Controllers and Functions#
##############################################################################

def loadBoard(data, fileName = "HerderLevel1.csv"):
	#reading the csv file
	reader2D = []
	with open(fileName, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			reader2D += [row]

	#converting strings in each cell into int
	readerInt = []
	for i in range(len(reader2D)):
		readerRow = []
		for j in range(len(reader2D[0])):
			# print(type(reader2D[i][j]))
			readerRow += [int(reader2D[i][j])]
		readerInt += [readerRow]
	data.board = readerInt
	
	data.sheep.loadSheep(data)
	data.shepherd.loadShepherd(data)
	data.wolf.loadWolf(data)


def drawBoard(canvas, data):
	for row in range(data.rows):
		for col in range(data.cols):
			drawCells(canvas, data, row, col)

def drawCells(canvas, data, row, col):

	gridWidth = data.width - 2 * data.margin
	gridHeight = data.height - 2 * data.margin
	
	cellWidth = gridWidth / data.cols
	cellHeight = gridHeight / data.rows

	x0 = data.margin + gridWidth * col / data.cols
	x1 = data.margin + gridWidth * (col+1) / data.cols
	y0 = data.margin + gridHeight * row / data.rows
	y1 = data.margin + gridHeight * (row+1) / data.rows

	canvas.create_image(x0,y0, image = data.grassPic, anchor = NW)
	# print(data.shepherd.no)
	if data.board[row][col] == -2:
		canvas.create_rectangle(x0, y0, x1, y1, fill="olive drab", width=0)
		canvas.create_image(x0,y0, image = data.hedgePic, anchor = NW)
	elif data.board[row][col] == data.wolf.no:
		canvas.create_oval(x0, y0, x1, y1, fill="dim grey", width=0)
		if data.wolf.direction == (-1,0):
			canvas.create_image(x0-10,y0-10, image = data.wolfPic, anchor = NW)
		elif data.wolf.direction == (0,1):
			canvas.create_image(x0-10,y0-5, image = data.wolfPicR, anchor = NW)
		elif data.wolf.direction == (0,-1):
			canvas.create_image(x0-10,y0-5, image = data.wolfPicL, anchor = NW)
		else:
			canvas.create_image(x0-10,y0-5, image = data.wolfPicB, anchor = NW)
	elif data.board[row][col] in (5,50):
		canvas.create_oval(x0, y0, x1, y1, fill="azure", width=0)
		if data.sheep.direction == (-1,0):
			canvas.create_image(x0-10,y0-7.5, image = data.sheepPic, anchor = NW)
		elif data.sheep.direction == (0,1):
			canvas.create_image(x0-10,y0-7.5, image = data.sheepPicR, anchor = NW)
		elif data.sheep.direction == (0,-1):
			canvas.create_image(x0-10,y0-7.5, image = data.sheepPicL, anchor = NW)
		else:
			canvas.create_image(x0-10,y0-7.5, image = data.sheepPicB, anchor = NW)
	elif data.board[row][col] == 50:
		canvas.create_image(x0-10,y0-7.5, image = data.sheepPic, anchor = NW)
	elif data.board[row][col] == 15:
		canvas.create_oval(x0, y0, x1, y1, fill="deep sky blue", width=0)
		canvas.create_image(x0-10,y0-7.5, image = data.shepherdPic, anchor = NW)
		canvas.create_oval(x0, y0-15, x1, y1-15, fill="azure", width=0)
		canvas.create_image(x0-10,y0-27.5, image = data.sheepPic, anchor = NW)
	#drawing the shepherd comes after drawing the shepherd with animal
	elif data.board[row][col] == data.shepherd.no:
		canvas.create_oval(x0, y0, x1, y1, fill="deep sky blue", width=0)
		if data.shepherd.direction == (-1,0):
			canvas.create_image(x0-10,y0-7.5, image = data.shepherdPic, anchor = NW)
		elif data.shepherd.direction == (0,1):
			canvas.create_image(x0-10,y0-5, image = data.shepherdPicR, anchor = NW)
		elif data.shepherd.direction == (0,-1):
			canvas.create_image(x0-10,y0-5, image = data.shepherdPicL, anchor = NW)
		else:
			canvas.create_image(x0-10,y0-5, image = data.shepherdPicB, anchor = NW)
		
	elif data.board[row][col] == 1: 
		canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab2", width=0)
	elif data.board[row][col] == -1:
		# canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab3", width=0)
		canvas.create_image(x0,y0, image = data.entryPic, anchor = NW)
	elif data.board[row][col] == -5:
		canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab2", outline="olivedrab3")
		canvas.create_image(x0,y0, image = data.safeZonePic, anchor = NW)

	if (data.debugMode):
		canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
						   text=str(data.board[row][col]),fill="grey",
						   font=("Helvatica", 14, "bold"))
	if (data.showMode):
		canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
						   text=str(row)+ ','+ str(col),fill="grey",
						   font=("Helvatica", 10, "bold"))

def drawScore (canvas, data):
	canvas.create_text(data.width/10, data.margin/2, text = "SCORE: %d" % data.score)
	canvas.create_text(data.width/10 * 9, data.margin/2, text = "LIVES: %d" % data.lives)
	if data.gameOver:
		drawGameOver(canvas, data)
	if data.nextLevel:
		drawNextLevel(canvas,data)

def chooseContinueOrQuit(event, data):
	x,y = event.x, event.y
	if (data.width/2-data.margin*5 < x and x<data.width/2-data.margin*0.5) and (data.height/2 <y and y<data.height/2 + data.margin):
		filename =  filedialog.askopenfilename(initialdir = "Levels",title = "Select file",filetypes = (('Csv file','*.csv'), ('All files','*.*')))
		try:
			loadBoard(data, filename)
		except:
			loadBoard(data, "Levels/HerderLevel4.csv")
		data.nextLevel = False
	elif (data.width/2+data.margin*0.5 < x and x<data.width/2+data.margin*5) and (data.height/2<y and y<data.height/2 + data.margin):
		score = ","+ str(data.score)
		old = data.highScoresFile.read()
		data.highScoresFile.write(old + score)
		init(data)

def chooseRestartOrQuit(event, data):
	x,y = event.x, event.y
	if (data.width/2-data.margin*5 < x and x<data.width/2-data.margin*0.5) and (data.height/2<y and y<data.height/2 + data.margin):
		score = "," + str(data.score)
		old = data.highScoresFile.read()
		data.highScoresFile.write(old + score)
		init(data)
	elif (data.width/2+data.margin*0.5 < x and x<data.width/2+data.margin*5) and (data.height/2<y and y<data.height/2 + data.margin):
		score = "," + str(data.score)
		old = data.highScoresFile.read()
		data.highScoresFile.write(old + score)
		init(data)

def chooseDifficulty(event, data):
	x, y = event.x, event.y
	if (data.width//2 - data.margin*3<x and x< data.width//2 + data.margin*3) and (data.margin*8<y and y<data.margin*9.5):
		data.difficultyEasy = True
		data.gameDifficultyMode = False
	elif (data.width//2 - data.margin*3<x and x<data.width//2 + data.margin*3) and (data.margin*10<y and y<data.margin*11.5):
		data.difficultyHard = True
		data.gameDifficultyMode = False
	elif (data.width//2 - data.margin*3<x and x<data.width//2 + data.margin*3) and (data.margin*12<y and y<data.margin*13.5):
		data.difficultyMulti = True
		data.gameDifficultyMode = False


def drawNextLevel(canvas, data):
	canvas.create_rectangle(data.width/2-data.margin*7, data.height/2- data.margin*3, data.width/2+data.margin*7, data.height/2+ data.margin*3, fill = "oliveDrab2", width = 10, outline = "oliveDrab4")
	canvas.create_text(data.width/2, data.height/2- data.margin, text = "YOU MADE IT TO THE NEXT LEVEL!", font = "System 24", fill = "dim grey")
	canvas.create_rectangle(data.width/2-data.margin*5, data.height/2, data.width/2-data.margin*0.5, data.height/2 + data.margin, fill = "oliveDrab3", width = 0)
	canvas.create_rectangle(data.width/2+data.margin*0.5, data.height/2, data.width/2+data.margin*5, data.height/2 + data.margin, fill = "oliveDrab3", width = 0)
	canvas.create_text(data.width/2, data.height/2+ data.margin//2, text = "CONTINUE\t\t\tQUIT\t", font = "System 12", fill = "black")
	canvas.create_text(data.width/2, data.height/2+ data.margin*1.5 , text = "* choose level after selecting 'continue' *", font = "System 12", fill = "dim grey")
	# data.nextLevel = False

def drawGameOver(canvas, data):
	canvas.create_rectangle(data.width/2-data.margin*7, data.height/2- data.margin*3, data.width/2+data.margin*7, data.height/2+ data.margin*3, fill = "oliveDrab2", width = 10, outline = "oliveDrab4")
	canvas.create_text(data.width/2, data.height/2- data.margin, text = "G A M E     O V E R", font = "System 36", fill = "black")
	canvas.create_text(data.width/2, data.height/2 + data.margin * 2, text = "* you ran out of lives *", font = "System 12", fill = "dim grey")
	canvas.create_rectangle(data.width/2-data.margin*5, data.height/2, data.width/2-data.margin*0.5, data.height/2 + data.margin, fill = "oliveDrab3", width = 0)
	canvas.create_rectangle(data.width/2+data.margin*0.5, data.height/2, data.width/2+data.margin*5, data.height/2 + data.margin, fill = "oliveDrab3", width = 0)
	canvas.create_text(data.width/2, data.height/2+ data.margin//2, text = "RESTART\t\t\tQUIT\t", font = "System 12", fill = "black")

# WOLF SMARTER AI

def bfs(board, startRow, startCol):
	visitedSet = set()
	childToParent = dict()
	queue = [(startRow, startCol)]

	while queue:
		(row,col) = queue.pop()
		neighborsList = neighbors(board, row, col)
		for (childRow, childCol) in neighborsList:
			if (childRow, childCol) not in visitedSet:
				if (childRow, childCol) not in childToParent:
					childToParent[(childRow, childCol)] = (row, col)
					if board[childRow][childCol] == 5:
						return pathTaken(childToParent, startRow, startCol, childRow, childCol)
					queue.insert(0, (childRow, childCol))
		visitedSet.add((row, col))
	return []

def neighbors(board, row, col):
	dirs = [(-1,0), (1,0), (0,-1), (0,1)]
	result =[]
	for dir in dirs:
		newRow = row + dir[0]
		newCol = col + dir[1]

		if (0 <= newRow and newRow < len(board)) and (0 <= newCol and newCol < len(board[0])):
			if board[newRow][newCol] in (0,5,10):
				result += [(newRow, newCol)]

	return result

def pathTaken(childToParent, startRow, startCol, row, col):
	resultList = [(row,col)]
	while (row,col) != (startRow, startCol):
		resultList += [childToParent[(row, col)]]
		(row, col) = childToParent[(row, col)]
	return resultList[::-1]

def checkLevelUp(data):
	for row in range(data.rows):
			for col in range(data.cols):
				if data.board[row][col] in (5,15):
					return False
	return True

#GENERATOR MODE FUNCTIONS

def generator_drawBoard(canvas, data):
	for row in range(data.generator_rows):
		for col in range(data.generator_cols):
			generator_drawCells(canvas, data, row, col)

def generator_drawCells(canvas, data, row, col):

	gridWidth = data.width - 2 * data.margin
	gridHeight = data.height - 2 * data.margin
	
	cellWidth = gridWidth / data.generator_cols
	cellHeight = gridHeight / data.generator_rows

	x0 = data.margin + gridWidth * col / data.generator_cols
	x1 = data.margin + gridWidth * (col+1) / data.generator_cols
	y0 = data.margin + gridHeight * row / data.generator_rows
	y1 = data.margin + gridHeight * (row+1) / data.generator_rows

	canvas.create_rectangle(x0, y0, x1, y1, fill="olivedrab2", outline="olivedrab1")
	# print(data.shepherd.no)
	if data.generator_board[row][col] == data.hedges.no:
		canvas.create_rectangle(x0, y0, x1, y1, fill="olive drab", width=0)
	elif data.generator_board[row][col] == 5:
		canvas.create_oval(x0, y0, x1, y1, fill="azure", width=0)
	elif data.generator_board[row][col] == 0: 
		canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab2", outline="olivedrab1")
	elif data.generator_board[row][col] == data.safeZoneEntry.no:
		canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab3", width=0)
	elif data.generator_board[row][col] == data.safeZone.no:
		canvas.create_rectangle(x0,y0,x1,y1, fill = "olivedrab2", outline="olivedrab3")
	if (data.checkMode):
		canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
						   text=str(data.generator_board[row][col]),fill="grey",
						   font=("Helvatica", 14, "bold"))

def drawMode(canvas, data):
	if data.hedgeMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "DRAW HEDGES")
	elif data.portalsMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "DRAW PORTALS")
	elif data.safeZoneMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "DRAW SAFE ZONE")
	elif data.safeZoneEntryMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "DRAW SAFE ZONE ENTRY")
	elif data.safeZoneHedgeMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "DRAW SAFE ZONE HEDGE")
	elif data.eraseMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "ERASE")
	elif data.checkMode:
		canvas.create_text(data.width//2, data.height - data.margin//2, text = "CHECKING")

def convertGenerator_Board(data):
	generator_board = data.generator_board
	fileName = filedialog.asksaveasfilename(initialdir = "Levels",title = "Select file",filetypes = (('Csv file','*.csv'), ('All files','*.*')))

	#writing the csv file
	with open(fileName + '.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=' ')
		for row in generator_board:
			spamwriter.writerow(row)

	#reading the csv file
	reader2D = []
	with open(fileName + '.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			reader2D += [row]

	#converting strings in each cell into int
	readerInt = []
	for i in range(len(reader2D)):
		readerRow = []
		for j in range(len(reader2D[0])):
			readerRow += [int(reader2D[i][j])]
		readerInt += [readerRow]


def drawHeader(canvas, data):
	canvas.create_text(data.width//2, data.margin//2, text="PRESS i FOR INSTRUCTIONS")

def drawInstruction (canvas, data):
	canvas.create_rectangle(data.margin *7, data.margin *6, data.width - data.margin*7, data.height - data.margin*6, fill = "oliveDrab1", width =10, outline = "oliveDrab3")
	canvas.create_text(data.width//2 , data.margin * 7, text = "I N S T R U C T I O N S", font = "Helvetica 12 underline")
	canvas.create_text(data.width//2 , data.height//2, text = 
		"\t1. press 'h' to build HEDGES \
		\n\n\t2. press 'p' to build PORTALS\
		\n\n\t3. press 's' to build SAFE ZONE\
		\n\n\t4. press 'a' to build SAFE ZONE HEDGES\
		\n\n\t5. press 'f' to build SAFE ZONE ENTRANCES\
		\n\n\t6. press 'e' to ERASE\
		\n\n\t7. press 'r' to SAVE WHEN YOU ARE DONE")
	canvas.create_text(data.width//2 , data.height-data.margin * 6.5, text = "** FOR NOW, PRESS 'i' to START BUILDING **")

def drawDifficulty (canvas, data):
	canvas.create_rectangle(data.margin *7, data.margin *5, data.width - data.margin*7, data.height - data.margin*6, fill = "oliveDrab1", width =10, outline = "oliveDrab3")
	canvas.create_text(data.width//2, data.margin * 7, text = "C H O O S E    M O D E", font = "system 18 bold underline", fill="dim grey")
	canvas.create_rectangle(data.width//2 - data.margin*3, data.margin*8, data.width//2 + data.margin*3, data.margin*9.5, width = 2, outline = "dim grey")
	canvas.create_rectangle(data.width//2 - data.margin*3, data.margin*10, data.width//2 + data.margin*3, data.margin*11.5, width = 2, outline = "dim grey")
	canvas.create_rectangle(data.width//2 - data.margin*3, data.margin*12, data.width//2 + data.margin*3, data.margin*13.5, width = 2, outline = "dim grey")
	canvas.create_text(data.width//2, data.margin * 8.75, text = "SMART WOLF", fill = "dim grey")
	canvas.create_text(data.width//2, data.margin * 10.75, text = "SMARTER WOLF", fill = "dim grey")
	canvas.create_text(data.width//2, data.margin * 12.75, text = "MULTIPLAYER", fill = "dim grey")
	canvas.create_text(data.width//2, data.margin * 14, text = "* multiplayer controls wolf with <a, w, s, d>  *", font = "system 12", fill = "dim grey")



	############################################################################################################

# the extra window widgets functions
def showEntryFields():
	data.fileName = "%s.csv" % (E1.get())
	E1.delete(0,END)

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
	elif (data.mode == "playGame"):   playGameMousePressed(event, data)
	elif (data.mode == "help"):       helpMousePressed(event, data)
	elif (data.mode == "generator"):       generatorMousePressed(event, data)
	elif (data.mode == "highScore"):       highScoreMousePressed(event, data)

def mouseMotion(event, data):
	if (data.mode == "splashScreen"): splashScreenMouseMotion(event,data)
	# data.motionPosn = (event.x, event.y)
	pass

def leftMoved(event, data):
	if (data.mode == "generator"): generatorLeftMoved(event,data)
	# data.leftPosn = (event.x, event.y)
	pass

def keyPressed(event, data):
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "help"):       helpKeyPressed(event, data)
	elif (data.mode == "generator"):       generatorKeyPressed(event, data)
	elif (data.mode == "highScore"):       highScoreKeyPressed(event, data)

def timerFired(data):
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "help"):       helpTimerFired(data)
	elif (data.mode == "generator"):       generatorTimerFired(data)
	elif (data.mode == "highScore"):       highScoreTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "help"):       helpRedrawAll(canvas, data)
	elif (data.mode == "generator"):       generatorRedrawAll(canvas, data)
	elif (data.mode == "highScore"):       highScoreRedrawAll(canvas, data)

####################################
# splashScreen mode
#################################### 

def drawMovingSplash(canvas, data):
	if data.splashTimerCount == 0:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen1Pic)
	elif data.splashTimerCount == 1:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen2Pic)
	elif data.splashTimerCount == 2:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen3Pic)
	elif data.splashTimerCount == 3:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen4Pic)
	elif data.splashTimerCount == 4:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen3Pic)
	elif data.splashTimerCount == 5:
		canvas.create_image(data.width//2, data.height//2, image = data.splashScreen2Pic)

def drawTitleButtons(canvas, data):
	canvas.create_rectangle(data.margin//2, data.margin//2, data.width - data.margin//2, data.height -data.margin//2, width = 10, outline = "white")
	canvas.create_rectangle(data.margin *5, data.height//2 - data.margin*5, data.width - data.margin*5, data.height//2 - data.margin*1.5, fill = None, width=5, outline="white")
	canvas.create_text(data.width/2, data.height/2 - data.margin *2,
					   text="S H E P H E R D  //  S A V I O R", font = "System 30 bold", fill = "white")
	canvas.create_rectangle(data.margin *5, data.height//2 - data.margin, data.width//2 - data.margin, data.height//2 + data.margin*2, fill = None, width=5, outline="white")
	canvas.create_rectangle(data.width - data.margin *5, data.height//2 - data.margin, data.width//2 + data.margin, data.height//2 + data.margin*2, width=5, outline="white")
	canvas.create_rectangle(data.margin *5, data.height//2 + data.margin*3, data.width//2 - data.margin, data.height//2 + data.margin*6, width=5, outline="white")
	canvas.create_rectangle(data.width - data.margin *5, data.height//2 + data.margin*3, data.width//2 + data.margin, data.height//2 + data.margin*6, width=5, outline="white")
	canvas.create_text(data.width//2 - data.margin*4.5, data.height//2 + data.margin*1.55, text="P L A Y", fill = "white", font = "System 20 bold")
	canvas.create_text(data.width//2 + data.margin*4.5, data.height//2 + data.margin*1.55, text="H E L P", fill = "white", font = "System 18 bold")
	canvas.create_text(data.width//2 - data.margin*4.5, data.height//2 + data.margin*5.6, text="D I Y   B O A R D", fill = "white", font = "System 18 bold")
	canvas.create_text(data.width//2 + data.margin*4.5, data.height//2 + data.margin*5.6, text="S C O R E S", fill = "white", font = "System 18 bold")
	
def drawMouseOnTitleButtons(canvas, data):
	if data.mouseOnPlay:
		canvas.create_rectangle(data.margin *5, data.height//2 - data.margin, data.width//2 - data.margin, data.height//2 + data.margin*2, fill = "white", width=5, outline="white")
		canvas.create_text(data.width//2 - data.margin*4.5, data.height//2 + data.margin*1.55, text="P L A Y", fill = "dim grey", font = "System 20 bold")
	elif data.mouseOnHelp:
		canvas.create_rectangle(data.width - data.margin *5, data.height//2 - data.margin, data.width//2 + data.margin, data.height//2 + data.margin*2, width=5, fill = "white", outline="white")
		canvas.create_text(data.width//2 + data.margin*4.5, data.height//2 + data.margin*1.55, text="H E L P", fill = "dim grey", font = "System 18 bold")
	elif data.mouseOnDIY:
		canvas.create_rectangle(data.margin *5, data.height//2 + data.margin*3, data.width//2 - data.margin, data.height//2 + data.margin*6, width=5, fill = "white", outline="white")
		canvas.create_text(data.width//2 - data.margin*4.5, data.height//2 + data.margin*5.6, text="D I Y   B O A R D", fill = "dim grey", font = "System 18 bold")
	elif data.mouseOnScore:
		canvas.create_rectangle(data.width - data.margin *5, data.height//2 + data.margin*3, data.width//2 + data.margin, data.height//2 + data.margin*6, width=5, fill = "white", outline="white")
		canvas.create_text(data.width//2 + data.margin*4.5, data.height//2 + data.margin*5.6, text="S C O R E S", fill = "dim grey", font = "System 18 bold")

def splashScreenMousePressed(event, data):
	x, y = event.x, event.y
	if (data.margin *5 < x and x < data.width//2 - data.margin) and (data.height//2 - data.margin < y and y < data.height//2 + data.margin*2):
		data.mode = "playGame"
	elif (data.width - data.margin *5 > x and x > data.width//2 + data.margin) and (data.height//2 - data.margin< y and y < data.height//2 + data.margin*2):
		data.mode = "help"
	elif (data.margin *5< x and x <data.width//2 - data.margin) and (data.height//2 + data.margin*3< y and y <data.height//2 + data.margin*6):
		data.mode = "generator"
	elif (data.width - data.margin *5> x and x >data.height//2 + data.margin*3) and (data.width//2 + data.margin< y and y <data.height//2 + data.margin*6):
		data.mode = "highScore"

def splashScreenMouseMotion(event, data):
	x, y = event.x, event.y
	if (data.margin *5 < x and x < data.width//2 - data.margin) and (data.height//2 - data.margin < y and y < data.height//2 + data.margin*2):
		data.mouseOnPlay = True
		(data.mouseOnHelp,data.mouseOnDIY, data.mouseOnScore)  = (False, False, False)
	elif (data.width - data.margin *5 > x and x > data.width//2 + data.margin) and (data.height//2 - data.margin< y and y < data.height//2 + data.margin*2):
		data.mouseOnHelp = True
		(data.mouseOnPlay,data.mouseOnDIY, data.mouseOnScore)  = (False, False, False)
	elif (data.margin *5< x and x <data.width//2 - data.margin) and (data.height//2 + data.margin*3< y and y <data.height//2 + data.margin*6):
		data.mouseOnDIY = True
		(data.mouseOnPlay,data.mouseOnHelp, data.mouseOnScore)  = (False, False, False)
	elif (data.width - data.margin *5> x and x >data.height//2 + data.margin*3) and (data.width//2 + data.margin< y and y <data.height//2 + data.margin*6):
		data.mouseOnScore = True
		(data.mouseOnPlay,data.mouseOnDIY, data.mouseOnHelp)  = (False, False, False)


def splashScreenKeyPressed(event, data):
	pass

def splashScreenTimerFired(data):
	data.splashTimerCount +=1
	data.splashTimerCount %= 6

def splashScreenRedrawAll(canvas, data):
	drawMovingSplash(canvas, data)
	drawTitleButtons(canvas, data)
	drawMouseOnTitleButtons(canvas, data)


####################################
# generator mode
####################################

def generatorMousePressed(event, data):
	if data.hedgeMode:
		data.hedges.place(event, data)
	elif data.eraseMode:
		data.erase.place(event, data)
	elif data.portalsMode:
		data.portals.place(event, data)
	elif data.safeZoneMode:
		data.safeZone.place(event, data)
	elif data.safeZoneHedgeMode:
		data.safeZoneHedge.place(event, data)
	elif data.safeZoneEntryMode:
		data.safeZoneEntry.place(event, data)
	
	x, y = event.x, event.y

	if (data.width//6 - data.margin * 3.375<x and x<data.width//6 + data.margin * 3 *5.25) and (data.height - data.margin<y and y<data.height):
		init(data)

def generatorLeftMoved(event, data):
	if data.hedgeMode:
		data.hedges.place(event, data)
	elif data.eraseMode:
		data.erase.place(event, data)
	elif data.portalsMode:
		data.portals.place(event, data)
	elif data.safeZoneMode:
		data.safeZone.place(event, data)
	elif data.safeZoneHedgeMode:
		data.safeZoneHedge.place(event, data)
	elif data.safeZoneEntryMode:
		data.safeZoneEntry.place(event, data)


def generatorKeyPressed(event, data):
	data.mainMode = False
	if event.char == "d":
		data.checkMode = not data.checkMode
	elif event.char == "h":
		data.hedgeMode = True
		data.eraseMode = False
		data.portalsMode = False
		data.safeZoneMode = False
		data.safeZoneHedgeMode = False
		data.safeZoneEntryMode = False
	elif event.char == "e":
		data.eraseMode = True
		data.hedgeMode = False
		data.portalsMode = False
		data.safeZoneMode = False
		data.safeZoneHedgeMode = False
		data.safeZoneEntryMode = False
	elif event.char == "p":
		data.portalsMode = True
		data.hedgeMode = False
		data.eraseMode = False
		data.safeZoneMode = False
		data.safeZoneHedgeMode = False
		data.safeZoneEntryMode = False
	elif event.char == "s":
		data.safeZoneMode = True
		data.hedgeMode = False
		data.eraseMode = False
		data.portalsMode = False
		data.safeZoneHedgeMode = False
		data.safeZoneEntryMode = False
	elif event.char == "a":
		data.safeZoneHedgeMode = True
		data.hedgeMode = False
		data.eraseMode = False
		data.portalsMode = False
		data.safeZoneMode = False
		data.safeZoneEntryMode = False
	elif event.char == "f":
		data.safeZoneEntryMode = True
		data.hedgeMode = False
		data.eraseMode = False
		data.portalsMode = False
		data.safeZoneMode = False
		data.safeZoneHedgeMode = False

	if event.char == "i":
		data.instructionMode = not data.instructionMode

	if event.char == "r":
		convertGenerator_Board(data)

def generatorTimerFired(data):
	pass

def generatorRedrawAll(canvas, data):
	generator_drawBoard(canvas, data)
	drawMode(canvas, data)
	drawHeader(canvas, data)
	if data.instructionMode:
		drawInstruction(canvas, data)
	canvas.create_rectangle(data.width//6 - data.margin * 3.375, data.height - data.margin, data.width//6 + data.margin * 3, data.height, fill = "oliveDrab1", width = 5, outline = "oliveDrab3")
	canvas.create_text(data.width//6, data.height-data.margin//2, text = "BACK HOME")

####################################
# help mode
####################################

def helpMousePressed(event, data):
	x, y = event.x, event.y
	if (data.width//6 - data.margin * 3.375<x and x<data.width//6 + data.margin * 3 *5.25) and (data.height - data.margin<y and y<data.height):
		init(data)

def helpKeyPressed(event, data):
	data.helpTimeCount +=1

def helpTimerFired(data):
	pass

def helpRedrawAll(canvas, data):
	left = data.margin
	top = data.margin
	right = data.width - data.margin
	bottom = data.height - data.margin
	canvas.create_rectangle(data.margin, data.margin, data.width-data.margin, data.height-data.margin, fill = "oliveDrab2", width=0)
	canvas.create_rectangle(data.width//6 - data.margin * 3.375, data.height - data.margin, data.width//6 + data.margin * 3, data.height, fill = "oliveDrab1", width = 5, outline = "oliveDrab3")
	canvas.create_text(data.width//6, data.height-data.margin//2, text = "BACK HOME")
	canvas.create_text(data.width/2, top*2, text = "I N S T R U C T I O N S", font = "system 30 bold underline")
	canvas.create_text(data.width/2, top*3, text = "press any <key> to proceed", font = "system 16", fill = "dim grey")
	if data.helpTimeCount >= 0:
		canvas.create_image(left*4, top*5, image = data.shepherd120Pic)
		canvas.create_image(right- left*3, top*5, image = data.shepherd120Pic)
		canvas.create_text(data.width/2, top*4.5, text = "This  is  a  S H E P H E R D", font = "system 20")
		canvas.create_text(data.width/2, top*5.5, text = "move the shepherd using arrow keys ", font = "system 20")
	if data.helpTimeCount >= 1:
		canvas.create_image(left*4, top*9, image = data.sheep120Pic)
		canvas.create_image(right- left*3, top*9, image = data.sheep120Pic)
		canvas.create_text(data.width/2, top*7.5, text = "This  is  a  S H E E P", font = "system 20")
		canvas.create_text(data.width/2, top*8.5, text = "S A V E   T H E M ", font = "system 20")
		canvas.create_text(data.width/2, top*9.5, text = "by picking and placing each O N E into the safe zone! ", font = "system 16")
	if data.helpTimeCount >= 2:
		canvas.create_image(left*4, top*13.5, image = data.wolf120Pic)
		canvas.create_image(right- left*3, top*13.5, image = data.wolf120Pic)
		canvas.create_text(data.width/2, top*12.5, text = "This   is   a   W O L F", font = "system 20")
		canvas.create_text(data.width/2, top*13.5, text = "THEY  A T T A C K  THE  S H E E P S ", font = "system 20")
		canvas.create_text(data.width/2, top*14.5, text = "they will  K I L L  Y O U too", font = "system 16")
	if data.helpTimeCount >= 3:
		canvas.create_image(left*4, top*17.5, image = data.entryPic)
		canvas.create_image(right- left*3, top*17.5, image = data.entryPic)
		canvas.create_text(data.width/2, top*16.5, text = "* S A V E  T H E  S H E E P S *", font = "system 20")
		canvas.create_text(data.width/2, top*17.5, text = "* A V O I D  T H E  W O L F *", font = "system 20")
		canvas.create_text(data.width/2, top*18.5, text = "* P L A Y  F O R E V E R *", font = "system 20") 


####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
	x, y = event.x, event.y
	if data.gameDifficultyMode:
		chooseDifficulty(event, data)
	if (data.width//6 - data.margin * 3.375<x and x<data.width//6 + data.margin * 3 *5.25) and (data.height - data.margin<y and y<data.height):
		init(data)
	if data.gameOver:
		chooseRestartOrQuit(event, data)
	elif data.nextLevel:
		chooseContinueOrQuit(event, data)

def playGameKeyPressed(event, data):
	if (event.char == "r"): 
		init(data) #reset
	elif (event.char == "p"): 
		data.paused = not data.paused; return #toggle between two
	elif (event.char == "b"):
		data.debugMode = not data.debugMode
	elif (event.char == "v"):
		data.showMode = not data.showMode

	if (data.gameOver or data.paused): 
		return

	if data.difficultyMulti:
		data.wolf.controlledMove(event, data)
	
	if not data.shepherd.dead:
		data.shepherd.move(event, data)


def playGameTimerFired(data):
	if not data.gameDifficultyMode:
		if data.gameOver == False:
			if data.shepherd.dead:
				data.shepherd.revive(data)
			data.sheepCounter += 1
			data.wolfCounter += 1
			data.sheep.move(data)
			if not data.difficultyMulti:
				data.wolf.move(data)
		
		if data.lives == 0:
			data.gameOver = True
		elif checkLevelUp(data):
			data.nextLevel = True
		

def playGameRedrawAll(canvas, data):
	drawBoard(canvas, data)
	drawScore(canvas, data)
	canvas.create_rectangle(data.width//6 - data.margin * 3.375, data.height - data.margin, data.width//6 + data.margin * 3, data.height, fill = "oliveDrab1", width = 5, outline = "oliveDrab3")
	canvas.create_text(data.width//6, data.height-data.margin//2, text = "BACK HOME")
	if data.gameDifficultyMode:
		drawDifficulty(canvas,data)

####################################
# highScore mode
####################################

def highScoreMousePressed(event, data):
	x, y = event.x, event.y
	if (data.width//6 - data.margin * 3.375<x and x<data.width//6 + data.margin * 3 *5.25) and (data.height - data.margin<y and y<data.height):
		init(data)

def highScoreKeyPressed(event, data):
	data.mode = "playGame"

def highScoreTimerFired(data):
	pass

def highScoreRedrawAll(canvas, data):
	canvas.create_rectangle(data.margin, data.margin, data.width-data.margin, data.height-data.margin, fill = "oliveDrab2", width=0)
	canvas.create_text(data.width//2 , data.margin * 6.5, text = "T O P  5  S C O R E S", font = "System 24 underline")
	for score in range(len(data.highScores)):
		if score < 5:
			canvas.create_text(data.width//2, 8 * data.margin + data.margin * score, text = "#%s.  " % (score+1) + data.highScores[score])

	canvas.create_rectangle(data.width//6 - data.margin * 3.375, data.height - data.margin, data.width//6 + data.margin * 3, data.height, fill = "oliveDrab1", width = 5, outline = "oliveDrab3")
	canvas.create_text(data.width//6, data.height-data.margin//2, text = "BACK HOME")

################################################################################################################################################
# use the run function as-is
################################################################################################################################################

def run(width=800, height=660):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    
 
	def mouseWrapper(mouseFn, event, canvas, data):
		if data.mouseWrapperMutex: return
		data.mouseWrapperMutex = True
		mouseFn(event, data)
		redrawAllWrapper(canvas, data)
		data.mouseWrapperMutex = False
 
	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)
 
	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

	# Set up data and call init
	class Struct(object): pass
	mixer.init()
	mixer.music.load("sound.mp3")
	mixer.music.play(-1)
	font.init()
	theMinionFont = font.SysFont("the minion.tff",25)
	data = Struct()
	data.mouseWrapperMutex = False
	data.width = width
	data.height = height
	data.timerDelay = 500
	root = Tk()
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mouseWrapper(mousePressed, event, canvas, data))
	canvas.bind("<Motion>", lambda event:
							mouseWrapper(mouseMotion, event, canvas, data))
	canvas.bind("<B1-Motion>", lambda event:
							mouseWrapper(leftMoved, event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("THANK YOU FOR PLAYING! . u . ")

	########################################################################
	
 
run()

##############################################################################
# citations
##############################################################################
# www.cs112.github.io
# https://docs.python.org/3.6/library/csv.html
# https://www.youtube.com/watch?v=IIENcvxadkI&feature=youtu.be
# https://pythonspot.com/en/tk-file-dialogs/
# https://www.khanacademy.org/computing/computer-science/algorithms/breadth-first-search/a/the-breadth-first-search-algorithm