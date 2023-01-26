# Minesweeper
#
# Modified for use in CS152 - Park University
# Original source code: https://github.com/ripexz/python-tkinter-minesweeper

from tkinter import *                                   # Importing other files or modules built in to python or from different file locations.
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

SIZE_X = 10                                             # Initializing the size of the game board
SIZE_Y = 10

STATE_DEFAULT = 0                                       # Initializing game staes for if nothing is happening on a tile, if the tile is being clicked, and if the tile is being flagged
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None                                           # Initialization of variables
images = None
frame = None
labels = None
wins = 0                                                # this is the number of times the user has won the game
secondChanceUsed = False
highestWinStreak = 0                                                 # keeps track of the highest win streak
currentWinStreak = 0                                                 # keeps track of the current win streak
lastWin = False                                         # whether or not the last game was won

def init():
        global images                                   # Any use of global variables is variables being pulled into a function so they may be accessed
        global labels
        global frame
        global window

        # import images
        images = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.gif"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "bomb": PhotoImage(file = "images/bomb.gif"),
            "numbers": []
        }
        for i in range(1, 9):                            # Depending on the number, apply a certian image to it
            images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

        # set up frame
        frame = Frame(window)
        frame.pack()

        # set up labels/UI
        labels = {
            "time": Label(frame, text = "00:00:00"),
            "mines": Label(frame, text = "Mines: 0"),
            "flags": Label(frame, text = "Flags: 0")
        }
        labels["time"].grid(row = 0, column = 0, columnspan = SIZE_Y) # top full width
        labels["mines"].grid(row = SIZE_X+1, column = 0, columnspan = int(SIZE_Y/2)) # bottom left
        labels["flags"].grid(row = SIZE_X+1, column = int(SIZE_Y/2)-1, columnspan = int(SIZE_Y/2)) # bottom right

        restart() # start game
        updateTimer() # init timer

def setup():
        global flagCount                                  # Variables being accessed within the function
        global correctFlagCount
        global clickedCount
        global startTime
        global tiles 
        global mines
        global images
        global frame
        global secondChanceUsed

        # create flag and clicked tile variables          # Certain variables are reset at game end     
        flagCount = 0
        correctFlagCount = 0
        clickedCount = 0
        startTime = None
        secondChanceUsed = False
        
        # create buttons
        tiles = dict({})
        mines = 0
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # tile image changeable for debug reasons:
                gfx = images["plain"]

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.1:
                    isMine = True
                    mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": Button(frame, image = gfx),
                    "mines": 0 # calculated after grid is built
                }

                tile["button"].bind(BTN_CLICK, onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, onRightClickWrapper(x, y))
                tile["button"].grid(row = x+1, column = y) # offset by 1 row for timer

                tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                mc = 0
                for n in getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                tiles[x][y]["mines"] = mc

def restart():                                            # Restarts the game and pulls from other functions to do so
        setup()
        refreshLabels()

def refreshLabels():                                      # Labels are refreshed
        global labels
        global flagCount
        global mines

        labels["flags"].config(text = "Flags: "+str(flagCount))
        labels["mines"].config(text = "Mines: "+str(mines))

def gameOver(won):                                        # Provide list of outcomes upon end of game
        global wins                                       # allows for use of wins variable within this function.
        global SIZE_X
        global SIZE_Y
        global tiles 
        global window
        global highestWinStreak
        global currentWinStreak
        global lastWin

        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if tiles[x][y]["isMine"] == False and tiles[x][y]["state"] == STATE_FLAGGED:
                    tiles[x][y]["button"].config(image = images["wrong"])
                if tiles[x][y]["isMine"] == True and tiles[x][y]["state"] != STATE_FLAGGED:
                    tiles[x][y]["button"].config(image = images["mine"])

        window.update()

        msg = None
        if won:                                            # Here is my 'imagination' application. Depending on whether or not the last game was won,
            lastWin = True                                 # The current win streak variable will be updated. If the current win streak variable is updated,
            currentWinStreak += 1                                       # if the current win streak variable is greater than the highest win streak variable, the highest win streak variable will be updated.
            if currentWinStreak > highestWinStreak:                                  # total wins are also incremented if the game is won, and if the game is lost then the current win streak variable is reset to zero
                highestWinStreak += 1
            wins += 1 # increments the wins counter
            msg = "You Win! Play again?"
        else:
            currentWinStreak = 0
            msg = "You Lose! Play again?"
            
        msg += """;
Wins: """ + str(wins)                                      # adds the "number of wins" string plus the literal number of wins to the winner or loser screen
        msg += """                                         
Current Win Streak: """ + str(currentWinStreak)                         # current win streak and highest win streak are also both added to the end game display screen
        msg += """
Highest Win Streak: """ + str(highestWinStreak)
        
        res = tkMessageBox.askyesno("Game Over", msg)
        if res:
            restart()
        else:
            window.quit()

def updateTimer():                                         # This function develops the timer and also updates it so that is actually runs
        global startTime
        global frame 
        global labels 

        ts = "00:00:00"
        if startTime != None: # if the game is running?
            delta = datetime.now() - startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        ts = "time elapsed: " + ts                  # adds "time elapsed" to the timer clock at top of game window
        labels["time"].config(text = ts) # sets the current time at the top of the window.
        frame.after(100, updateTimer)

def getNeighbors(x, y):                     #gets the surrounding tiles from the clicked coordinates        
        global tiles

        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

def onClickWrapper(x, y):                                              # get coordiantes of cliked tile
        global tiles

        return lambda Button: onClick(tiles[x][y])                     # lambda is a small anonymous function, can take arguments but only one expression 

def onRightClickWrapper(x, y):                                         # gets coordinates of tile that was right-clicked
        global tiles

        return lambda Button: onRightClick(tiles[x][y])

def onClick(tile):                                                     # This function provides a list of outcomes when a tile is clicked
        global startTime
        global images 
        global mines
        global clickedCount
        global secondChanceUsed
        if startTime == None:                                          # game clock starts
            startTime = datetime.now()

        if tile["isMine"] == True:                                     # This is where the 'second chance' is implemented. A second chance variable is initialized as False and also is reset when the game is over
            if secondChanceUsed == True:                               # If a mine is clicked the second chance varible is also updated to 'True'.
                # end game                                             # If second chance has been used and another mine is clicked, the game ends. 
                tile["button"].config(image = images["bomb"])
                gameOver(False)
                return
            else:
                tile["button"].config(image = images["mine"])         # mine image is displayed upon clicking mine
                tkMessageBox.showwarning('WARNING', 'Be Careful, you touched a mine!') # mine warning message is displayed upon clickin first mine
                secondChanceUsed = True                                # if the second chance has not been used and a mine is clicked then second chance becomes 'True' as in used.
        # change image
        elif tile["mines"] == 0:
            tile["button"].config(image = images["clicked"])
            clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image = images["numbers"][tile["mines"]-1])
            
        # if not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            clickedCount += 1
        if clickedCount == (SIZE_X * SIZE_Y) - mines:
            gameOver(True)

def onRightClick(tile):                                                 # This function provides a list of outcomes for when right click is used on a tile
        global startTime
        global images
        global flagCount
        global correctFlagCount

        if startTime == None:                                           # game clock starts
            startTime = datetime.now()

        # if not clicked
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                correctFlagCount += 1
            flagCount += 1
            refreshLabels()
        # if flagged, unflag
        elif tile["state"] == 2:
            tile["button"].config(image = images["plain"])
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                correctFlagCount -= 1
            flagCount -= 1
            refreshLabels()

def clearSurroundingTiles(id):                            # This function clears surrounding tiles upon clicking of a number
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in getNeighbors(x, y):
                clearTile(tile, queue)

def clearTile(tile, queue):                               # This function changes the tile image depending on if the state is now a number or mine. It also sets the status of the tile as clicked.
        global clickedCount
        global images

        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        clickedCount += 1

### END OF CLASSES ###

def main():
    global window

    # create Tk instance
    window = Tk()
    # set program title
    window.title("Minesweeper")
    # create game instance
    init()
    # run event loop
    window.mainloop()

if __name__ == "__main__":
    main()

