##############################################################################
Zoe Yee Teoh
15-112 Fundamentals of Programming
Section C
##############################################################################

> What is your project?
> How to install and run it
> How to download/install 3rd party libraries

###########################################################################
For my term project, I made a 2Dimensional game.

In the game, the player takes on the role of being a shepherd and the objective of the game is to ensure that all the animals in the field are in the safe zone before the wolf eats them up. To achieve the objectives of the game, the shepherd has to walk to the animal, pick them up and immediately transport them to the safe zone, which will be first located at the center of the “board”, where the board will represent the field.

The board consists of the safe zone, as mentioned earlier, as well as hedges along the borders of the field (refer to storyboard for a pictorial representation of the board). There are gaps along the hedges, which acts as portals. The top portal will transport the shepherd from the top of the field to the bottom of the field, vice versa. The right portal will transport the shepherd to the left of the field, vice versa.

The game ends when the shepherd ran out of lives. At the beginning of the game, the shepherd starts out with three lives. Every time the sheep or the shepherd gets eaten up by the wolf, the shepherd will lose a life.

At each stage, there will be a set number of sheep, with an increasing number of animals for the next stage. The stage ends when the shepherd successfully save all the animals present on the field for that stage. 

After each stage, the player can choose what board he/ she wants to play next. This includes a board that the player generate him/ herself, from the diy board option on the menu.

##############################################################################

since i am just using tkinter, there is no additional downloads needed to run the program

##############################################################################

no external libraries are used, and therefore, no additional software other than python and a text editor is needed

##############################################################################

##############################################################################

> Explain the problem, and how you solve it.
> Why you chose the particular functions, data
structures, algorithms that you used.
> Discuss the user interface choices.

##############################################################################

* the problem:
there isn’t a problem that prompted me to create this project. instead, there is an objective of entertaining the user and providing them with a sense of entertainment.

* my solution:
in order to entertain the user, a game must not be too hard to play, and not easy as well. 

in order to make the game have a certain level of difficulty, i made the AI of the wolf smarter by moving towards the closest animal. 

even though there is no timer counting down, there is a certain sense of urgency- to reach the animals before the wold does. 

##############################################################################

* the overall organisation of the game is using object oriented programming.

using this method, i am able to organise all the different characters- shepherd, sheep, wolf, as well as the landscape- the hedges, safe zone hedges, safe zone entry and portals. this would ensure a clearer code, with each of their methods placed separately and organised based on the class it is in. an example would be the load and move function, which is present in all of the character classes. this would prevent the overpopulation of the controllers and convolute the code.
———————————————————————————————————————————————————————————————————————————————————
* i decided to use a grid system. this meant that instead of moving a certain number of steps in a certain direction, the characters move by rows and cols. each 'step' taken would be equal distance for each character.

the problems of using a grid system is that it is less appealing, being bound to a grid system might make everything look very rigid. HOWEVER, i believe that the function of the program is more important as compared to the form of it. some may argue that the function would be enhanced with a better form, which i do agree. however, in my game, my level of proficiency in Python and the time frame, i believe it would be best for me to work with a grid system. Here are the reasons why:

- with a grid system, i will be able to keep track of the value of each cell, which corresponds to what is present on the cell- character or landscape feature. WHY IS THIS IMPORTANT? so i would be able to store all the values in a 2D list and this would make a DIY course possible
- though it is unappealing at first glance, the attractiveness can be enhanced by not having the grid lines to show. also, in the future, the grids can be smaller, and animals can occupy more than one cell (4 to create a similar square cell structure). this would then reduce the rigidity of the game.
- without a grid system, characters are able to move at different speed. HOWEVER, this is also possible for a grid system by having an additional time counter. in a NON GRID system, the time can be kept constant since the distance at each timer fired differs across characters. HOWEVER, in a GRID system, the distance of each move is kept constant, therefore, i am able to vary the "timer fired" indirectly by having an additional time counter, that increment each timer fired, and only when the time counter is a multiple of a value will i execute a move.
———————————————————————————————————————————————————————————————————————————————————
* i decided to make my game 2Dimensional, even though i proposed to have it to be pseudo 3Dimensional. Pseudo 3Dimensional means that i would be projecting a 3D object onto my 2D canvas. (so everything is flat, but i make it LOOK 3D)

HERE ARE THE REASONS WHY I CHOSE TO DO SO:
- i believe it is not a very efficient use of time. it would be more time efficient to use a 3D module like pandas or even pygame (possibly?) to make an actual 3D board
- a pseudo 3D board does not allow me to effectively implement collision detection, which is needed for my animals since they are moving randomly (not that they will walk into the hedge, but that it would not be effectively presented since there is no sense of what is in front and what is behind, as well and a sense of height- whether the sheep is higher or the hedges are higher)
- for players to have the authority to build their own course, there might be problems involving the animals being hidden by the hedges (assuming the representation of the board is MAGICALLY fixed and implemented) i believe that this creation of additional bugs is unnecessary just to make my product a little more physically appealing
———————————————————————————————————————————————————————————————————————————————————
* i decided to make the animals in my game move according to MARKOV'S CHAIN, a stochastic model describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. (taken from google.com)

the probability table i came out is shown below:

[	[0.2, 0.2, 0.2, 0.2, 0.2],
	[0.2, 0.3, 0.1, 0.2, 0.2],
	[0.2, 0.1, 0,3, 0.2, 0.2],
	[0.2, 0.2, 0.2, 0.3, 0,1],
	[0.2, 0.2, 0.2, 0.1, 0,3],	]

the row and col, which represents the next direction and the initial direction respectively, follows this list:
[(0,0), (0,1), (0,-1), (1,0), (-1,0)]

which can be translated as:
[‘None’, ‘Right’, ‘Left’, ‘Up’, ‘Down’]

in general, a guideline i used is that the probability of moving in the same direction is higher than anything else, a simple principle of inertia, where an object in motion will continue in motion in the same direction. a tendency to do nothing or to remain unchanged (taken from google.com) another guideline i have is that the chances of moving in the opposite direction should be less than the chances of moving in the other three directions. therefore, i came out with a model that the probability to staying in the same direction is 0.3, that of moving in the opposite direction is 0.1 and that of moving in the other direction is 0.2.

one edge case is if the initial direction is (0,0), which means the animal was stationary. in this case, there is no direction that is “opposite” of being stationary. instead, every other direction is opposite of of being stationary. also, another problem if i used the guidelines i made, the chances of the animals roaming freely would be lower, since there is a higher probability for them to stay stationary every single move. this is mainly because the sheep always starts with a direction of (0,0), being stationary when first placed on the board. this would make the game play very static and less challenging, which is why i decided to make an equal chance (p = 0,2) of it moving and being stationary.


(note: i converted the probability 2D list into one that stores the next direction taken, given the initial direction as the row index and the probability as the column index, where a 0.09 probability will land on column 0 and a 0.91 probability will land on column 9)
———————————————————————————————————————————————————————————————————————————————————
* i decided to make the wolf smarter than the sheep, by having it go to the closest sheep

the complexity in this is to be able to keep track of all the values- the distance from the wolf to the sheep using the MANHATTAN DISTANCE, which sheep is nearest to the wolf, the position of the sheep and the difference in the position of the sheep and the wolf. in order to do this, i kept all my variables in a dictionary- keeping track of which sheep i am calculating. also, this would determine the number of sheep on the board.

a problem arise since the safe zone is not accessible by the wolf. this acts as a barrier from the wolf to the sheep, which makes a simple calculation of the sum of the change in rows and cols between the wolf and sheep an inaccurate representation of the distance from the wolf to the sheep. instead, it only represents the displacement between the wolf and the sheep.

which is why...
———————————————————————————————————————————————————————————————————————————————————
* i decided to make a smarter AI for the wolf by using BREADTH FIRST SEARCH

i thought os using backtracking to find out the path to the sheep, however it would be very inefficient because the sheep would be constantly moving at every timer fired and backtracking requires the computer to check the entire board every timer fired. instead of a depth first search algorithm like backtracking, i decided to use a general breadth first search algorithm

there are definitely more complex breadth first search algorithms like dijkstra’s algorithm and A* algorithm but since the wolf is in a grid and cannot move diagonally, it means that the ‘nodes’ are equally weighted. this makes the two above mentioned algorithm slightly unnecessary. 

here is how the algorithm works:
- keeping track of the cells visited, i have a queue which is the cells i need to check as well as a child to parent dictionary to keep track of the child parent pair
- while there is still items in the queue, there are still cells that i have yet to checked, i would take one row, col cell coordinate out.
- i would then check what are the neighbours of this cell coordinate and add them to a list
- i would then check whether i have visited the neighbour cell and if it is not already in my child to parent dictionary.
- if the neighbour cell satisfy the two requirements, i would add that neighbour cell into my dictionary- with the neighbour cell coordinate as my key and the initial cell coordinate as my value
- this creates a child to parent pair
- this function ends once the wolf reaches the first sheep, with a dictionary with all the 
- if it does not reach the sheep yet, it would then insert this one neighbouring cell coordinate to the start of the list (because when we choose the initial cell coordinate to check, we take the last one in the list)
- we will also need to add the cell coordinates into the visited set so that we won’t be visiting the same cell more than once
- if the wolf does not reach the sheep, it would just return an empty list
		
- this dictionary returned gives all the possible child to parent pair, which means that there are a lot of additional tuples that are not useful
- a helper function would take in the dictionary and return a list containing tuples with each movement the wolf has to take to move towards the sheep
- how it does it is that it finds the value where the key is the sheep and the value will give the sheep cell’s parent cell. then, i would find the value where the key is the parent cell and the value will be the parent cell’s parent cell’s, which is the sheep cell’s grandparent. this function ends when it reaches the cell coordinate of the wolf.


