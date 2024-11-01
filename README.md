Title: Conway's Game of Life
Implemented and designed by: James Marciano
Project Video: https://youtu.be/O7f681etbKs

HARDWARE REQUIREMENTS:

Flask
Flask-Session

INTRODUCTION:

For my final project, I decided to implement Conway’s Game of Life, with a slight twist of having the ability to modify the cell’s behavior. Conway’s Game of Life is a pattern-building game and simultaneously a simulator for how creatures might live and expand in the real world. While the original Conway’s Game of Life is limited to strict rules, my version of Conway's Game of Life is extremely customizable. Not only can you change the behaviors of the cells but you can also change how big your grid is, and the time between generations. The addition of being able to change the fundamental rules of how the cells operate is a key difference between my version of Conway’s Game of Life and the classic version, and it allows for more insightful visions when it comes to seeing how species grow.

USAGE:

When a user first opens my website, they are greeted by a home screen with an animated gif in the background displaying one of the numerous patterns that can be created by the game. On this screen, the user is greeted with three buttons, one labeled “Play” that allows the user to enter the play space. Another is labeled “Rules & About” which will talk about the fundamental rules in the classic Conway’s Game of Life, and the last is labeled “Common Patterns” that offers three simple common patterns that people have discovered.

THE PLAYSPACE & SETTINGS:

The playspace consists of a grid of squares where all of the cells live and grow. This grid starts out with the minimum number of columns and rows needed to fully fit your screen, but this can be configured in settings which can be accessed by clicking the gear icon in the top right of the screen. When entering settings, the user is greeted by 6 text inputs that they can change the settings on how the game operates. The first two options allow the user to adjust the number of rows and columns that are on the screen, however these options can not be set to non-integer values or values less than the minimum number of columns or rows to fit the screen. However, it is important to note that there is no upper bound on the amount of rows and columns you can have, but inputting high numbers can generally cause the website to lag or even crash. The third setting allows the user to change the timing between generations, initiated by the run button on the top of the screen. Lastly, the three options on the bottom allow us to change the fundamental rules of Conway’s Game of Life and are what truly allows us to generate unique patterns.

RULES:

Conway’s Game of Life generates patterns on the basis that each cell has its fate decided by the 8 adjacent cells around it. The game operates on generations, where once the generation is incremented the rules will cause some cells to die, some cells to come back to life, and some cells to simply stay alive. The first general rule of Conway’s Game of Life is underpopulation. If a live cell does not have enough cells adjacent to it, it will die in the next generation due to underpopulation. This can be configured in settings on the fourth option where it states the minimum number of cells needed for a cell to stay alive, however it is set to 2 by default. The next rule of Conway’s Game of LIfe is overpopulation. If a live cell has far too many cells around it, it will die in the next generation due to overpopulation. This can also be configured in settings under the fifth option where it states the maximum number of cells needed for a cell to stay alive, however this is set to 3 by default. A live cell is able to survive into the next generation when it has greater than or equal to the criteria for underpopulation, and when it has less than or equal to the criteria for overpopulation, by default, a cell is able to survive into the next generation when it has 2-3 live cells adjacent to it. The final rule in Conway’s Game of Life is reproduction. When a dead cell has a certain amount of live cells next to it, that cell will come to life in the next generation. While this can be configured to settings, it is by default 3. These are the fundamental rules of Conway’s Game of Life, however it is important to note that the patterns displayed on the Common Patterns page only work when all rule settings are set to default.

STATISTICS:

In the playspace on the bottom of the screen there is a statistics overlay that keeps track of the current generation, how many cells are alive, and how many cells have died. It is important to note that the alive data only keeps track of how many cells are currently alive inside of the grid, while the death counter keeps track of all cells that have been dead. Also, when the program is paused, when manually clicking a live cell to kill it, this will not increase the death counter. These statistics create an interesting dynamic, and even oscillating patterns tend to have a lot of deaths.

TOOLS:

In order to run their simulations, the user has a number of tools at their disposal for convenience in testing and generating new patterns. The first tool is the STEP tool. This tool is used to move into the next generation by following the rules set by the user. The next tool is the RUN tool. This tool will repeatedly step into the next generation over a certain amount of seconds (assigned by the third option in settings). The next tool is the PAUSE tool, which is used to temporarily halt any ongoing simulations being run. It is important to note that when you pause the current simulation you are still able to add cells to the grid, and are even able to add cells to the grid while a simulation is ongoing (however, by the default rules the cell will immediately die). The PREVIOUS tool allows the user to revert to the grid they had before they ran their simulation. However, it will always be the grid right before running. This means that if you run, pause and then run your program again, only the most recently run grid will be saved. This will also reset the generation, alive, and dead count. The last tool at the user's disposal is the RESET tool. This will fully reset the grid, resetting all of the statistics and resetting all of the cells to be off.


COMMON ISSUES & RECOMMENDED USAGE:

One common issue that a lot of users face is trying to place cells while a simulation is already ongoing. When a simulation is on going, by the default rules, placing a cell will immediately result in its death. Therefore, if you ever want to generate a pattern but your cells immediately keep dying, make sure that the simulation isn’t already running. You will know if a simulation is running if the generation count on the bottom of the screen is increasing.

For first-time users, it is recommended to first read up on the rules and how patterns can develop. From here, I recommend testing out the three starter patterns inside of the Common Patterns page to see the possibilities that can be created by the simple default rules. Then, you can enter the playspace and start to create patterns yourself. From here you can change the fundamental rules, and start making new and unfound patterns!
