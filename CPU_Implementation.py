# CPU IMPLEMENTATION

from IPython.utils.path import random
from numba import cuda
from threading import *
import numpy as np
import math
import time

class Goat:
  def __init__(self):
    while (True):
      tempx = random.randrange(dim)
      tempy = random.randrange(dim)
      if (cells[tempy][tempx].lock.acquire(False)==True):
        self.x = tempx
        self.y = tempy
        print("Start Position: "+str(tempx) + ", " + str(tempy))
        break

class Cell:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.lock = Semaphore(1)
    #This item will hold the object that currently occupies that grid space, whether it is the wall of the pen, or another goat.
    #Then, when checking neighboring cells, we can just see if cell.item == null

#@cuda.jit
def move(goats,cells): #Placeholder function
  #thread = cuda.grid(1)
  for goat in goats:
    moves = 0
    attempts = 0
    while (True):
      attempts = attempts+1
      old_cell = cells[goat.y][goat.x]
      dir = random.randrange(4)
      match dir:
        case 0:
          dir = [1,0]
        case 1:
          dir = [0,1]
        case 2:
          dir = [-1,0]
        case 3:
          dir = [0,-1]
      new_cell = cells[dir[1]+old_cell.y][dir[0]+old_cell.x]
      if (new_cell.lock.acquire(False)==True):
        goat.x = new_cell.x
        goat.y = new_cell.y
        old_cell.lock.release()
        moves = moves+1
      print(str(goat.x)+ ", "+str(goat.y))
      if (goat.x == math.floor(dim/2) and goat.y == 0):
        new_cell.lock.release()
        print("Exit Found in " + str(moves) + " moves! (" + str(attempts)+ " Attempted moves)")
        break
    #time.sleep(1)

# Process for moving the goats is:
# 1. Check if an adjacent cell is unlocked, if not, select a new cell.
# 2. When it finds a cell that isn't locked, lock it.
# 3. Move to the newly locked cell.
# 4. Update internal cell info.
# 5. Unlock former cell.
# 6. If the new cell is the entrance to the pen, 'kill' the goat and the coresponding thread.

dim = 5
numgoats = 2

cells = np.array([[Cell(c,j) for c in range(dim)] for j in range(dim)])
for cellrow in cells:
  for cell in cellrow:
    print("["+str(cell.x)+", "+str(cell.y)+"]", end="")
    if (cell.x==0 or cell.x==dim-1 or cell.y==0 or cell.y==dim-1):
      if (cell.x != math.floor(dim/2) or cell.y != 0):
        cell.lock.acquire()
  print("")
print("Exit: "+str(math.floor(dim/2))+ ", 0")
print("")
goats = np.array([Goat() for c in range(numgoats)])
#move[1,numgoats](goats,cells)
move(goats,cells)
