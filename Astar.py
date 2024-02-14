# This function takes board as an input
# returns three lists as described in README file
# In board, following convention is followed
#         1 -> musketeer
#         2 -> soldier
#         0 -> empty location
#         3 -> Soldier With Diamond (Goal State)


# A* Search

import queue as Q

class node:
    def __init__(self, xc, yc, p, fx, fy, g):
        self.x = xc
        self.y = yc
        self.p = p
        self.f = abs(fx-xc)+abs(fy-yc)+g
        self.g = g

    def __eq__(self, other):
        if self.f == other.f:
            return 1
        else:
            return -1

    def __ne__(self, other):
        if self.f != other.f:
            return 1
        else:
            return -1

    def __lt__(self, other):
        if self.f < other.f:
            return 1
        else:
            return -1

    def __gt__(self, other):
        if self.f > other.f:
            return 1
        else:
            return -1

    def __le__(self, other):
        if (self.f < other.f) or (self.f == other.f):
            return 1
        else:
            return -1

    def __ge__(self, other):
        if (self.f > other.f) or (self.f == other.f):
            return 1
        else:
            return -1

def expand(en,fl,es,mat,fx,fy):
	'''
		This function expands the given node en and adds the children of en into the frontier list fl if they are not present 
		in the frontier list fl or the explored nodes set es.
	'''

	m=len(mat)
	n=len(mat[0])

	x=en.x
	y=en.y

	y-=1
	
	if y>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy,en.g+1))
	x+=1
	y+=1
	
	if x<m and y<n and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy,en.g+1))
	y+=1
	x-=1
	
	if y<n and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy,en.g+1))
	y-=1
	x-=1

	if y>=0 and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy,en.g+1))

	return fl


def Astar(board):
	'''
		This function implements the A* Search
	'''

	mat=board
	m=len(mat)
	n=len(mat[0])
	
	muske=[]

	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==3:
				fx=x
				fy=y

	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==1:
				muske.append(node(x,y,None,fx,fy,0))

	num=len(muske)      # num is the number of musketers
	
	EN=[]
	SQ=[]
	SP=[]
	for i in range(0,num):

		musk=muske[i]
		es=[]
		fl=Q.PriorityQueue()
		fl.put(musk)
		sq=[]
		s=[]
		while(1):
			if(fl.empty()):
				break
			en=fl.get()
			es.append(en)
			if mat[en.x][en.y]==3:
				break
			fl=expand(en,fl,es,mat,fx,fy)
			s=fl.queue
		
			t=[]
			for i in range(len(s)):
				t.append([s[i].x,s[i].y])
			 
			sq.append(t)
		s=fl.queue
		
		t=[]
		for i in range(len(s)):
			t.append([s[i].x,s[i].y])
		
		sq.append(t)
		est=[]
		for i in range(0,len(es)):
			est.append([es[i].x,es[i].y])
		
		path=[]
		par=en.p
		path.append([en.x,en.y])
		while(par):
			path.append([par.x,par.y])
			par=par.p

		path.reverse()

		if mat[en.x][en.y]==3:
			EN.append(est)
			SQ.append(sq)
			SP.append(path)

	# Returning the shortest path which is shortest among all the available musketers

	number=len(EN)
	mini=0
	if number>=2:
		if len(SP[0])<=len(SP[1]):
			mini=0
		else:
			mini=1

	if number==3:
		if len(SP[2])<=len(SP[mini]):
			mini=2
			
	if number==0:
		exploredNodes=[]
		searchQueue=[]
		shortestPath=[]
	else:
		exploredNodes = EN[mini]
		searchQueue  = SQ[mini]
		shortestPath = SP[mini]

	return (exploredNodes,searchQueue,shortestPath)

def convert_2d_matrix(input_file):
  """Converts a 2D matrix without commas and square brackets to a 2D array with commas and square brackets.

  Args:
    input_file: The path to the input file.

  Returns:
    A 2D array with commas and square brackets.
  """

  with open(input_file, "r") as f:
    matrix = f.read().splitlines()

  # Remove the square brackets from the matrix.
  matrix = [row.strip("[ ]") for row in matrix]

  # Split the matrix into rows and columns.
  rows = [row.split() for row in matrix]

  # Convert the rows to lists of integers.
  rows = [[int(x) for x in row] for row in rows]

  # Return the 2D array.
  return rows

input_file = "example.txt"
board = convert_2d_matrix(input_file)

output = [Astar(board)[i] for i in range(3)]
print("exploredNodes =", output[0])
print("searchQueue =", output[1])
print("shortestPath =", output[2])