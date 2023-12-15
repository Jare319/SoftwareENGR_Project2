# SoftwareENGR_Project2

FOR GPU IMPLEMENTATION:
Dependencies:
* numba.cuda
* numba.cuda.atomic
* numba.cuda.random
* numpy
* IPython.utils.path.random
* math

Installation:
Aside from Python and the above mentioned dependencies, nothing should need to be installed.

Usage:
Our simulation is resizeable, meaning the user can specify the number of goats and pen size. Currently these variables are only set from within the program, so a user must edit these variables to use a custom size. As it stands, the GPU code is currently set to use a pen size of 13x13 with 121 goats, which should provide an adequate test of the program. The maximum pen size is unknown, we tested it with 101x101 and it handled it without problem. The maximum number of goats is (dimension of the pen - 2)^2, which is where 121 comes from with a pen size of 13x13.

Verification:
Due to the fact that our program only writes and reads data from the GPU once each, instead of every clock cycle means that we didn't have an effective way to store the movement data of each goat. With that said, the output of the code can be verified by the data printed after the program is run. The output of the program should produce several arrays:
[cells] this array contains the matrix of cells in the pen. A 1 indicates it is either occupied, or part of the pen wall, while a 0 indicates that cell is empty.
[goats] this array contains a list of all the cells each goat was placed in. For example, the 0 index of this array may contain 62. That implies goat 0 was placed into cell 62 in the pen. Cells are numbered starting at 0 in the top left, increasing from left to right and top to bottom, with the bottom right cell being the largest, with a cell number of (dimension x dimension) - 1, or cell 168 for a 13x13 grid.
[cells2] this array contains the cells of the pen after the goats are placed into it. For 121 goats and a pen size of 13x13, this should be all 1s, implying every cell is occupied. The exception to this is that the pen should be "open", meaning the cell number corresponding to floor(dimension/2) should be the only cell with a 0.
[cells3] this array shows the pen after the goats have moved. It should be identical to the first array, implying that all the goats have escaped and the pen is empty again.
[goats2] this array shows the same goat array as before, indicating the current positions of each goat. When a goat escapes, its position value in this array is set to -1, indicating it has left the pen. If the program has executed successfully, this array should contain a -1 in every index.
[moves] this list is a parallel array with the goats list, indicating how many attempted moves it took the corresponding goat to make in its escape attempt.
