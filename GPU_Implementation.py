# GPU IMPLEMENTATION

from numba import cuda; cuda.atomic
import numba.cuda.random
import numpy as np
from IPython.utils.path import random
import math

@cuda.jit
def move(goats,cells,dim,rng_states,movements):
  thread = cuda.grid(1)
  while (goats[thread] != math.floor(dim/2)):
  #while (False):
    dir = math.floor(numba.cuda.random.xoroshiro128p_uniform_float32(rng_states, thread)*4)
    #dir = 1
    match dir:
      case 0:
        dir = goats[thread]-dim
      case 1:
        dir = goats[thread]+dim
      case 2:
        dir = goats[thread]-1
      case 3:
        dir = goats[thread]+1
    if (cuda.atomic.cas(cells,dir,0,1)==0):
      cells[goats[thread]] = 0
      goats[thread] = dir
    movements[thread] = movements[thread] + 1
  cells[goats[thread]] = 0
  goats[thread] = -1

dim = 13
numgoats = 121
#goats = cuda.device_array((numgoats,), int)
goats = np.zeros((numgoats,),np.int32)
for x in range(numgoats):
  goats[x]=0

#cells = cuda.device_array((dim*dim,), int)
cells = np.zeros((dim*dim,),np.int32)
for x in cells:
  cells[x]=0

rng_states = numba.cuda.random.create_xoroshiro128p_states(numgoats, seed=random.randint(0,1000))
for x in range(dim*dim):
  if (x<dim or x>(dim*dim)-dim or x%dim == 0 or (x+1)%dim ==0):
    cells[x] = 1

print(cells)
#print(cells.copy_to_host())
for x in range(numgoats):
  while (goats[x]==0):
    ind = np.random.randint(dim*dim)
    if (cells[ind] == 0):
      cells[ind]=1
      goats[x]=ind
cells[math.floor(dim/2)] = 0
movements = np.zeros((numgoats,),np.int32)

print(goats)
print(cells)
#print(goats.copy_to_host())
#print(cells.copy_to_host())
move[1,numgoats](goats,cells,dim,rng_states,movements)
print(cells)
print(goats)
print(movements)
