#################################################
# hw8.py
# author: Roshan Ram
#################################################
import math, copy, time, random
from cmu_112_graphics import *
from tkinter import *


#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    #from http://www.cs.cmu.edu/~112/notes/
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    #from http://www.cs.cmu.edu/~112/notes/
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    
######################################################

# sidescroller thing starts here

#splash screen 

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        flashingColorList = ['coral1', 'bisque', 'lightblue1']
        color = flashingColorList[random.randint(0, len(flashingColorList)-1)]
        font = 'Arial 26 bold'
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
        fill='palegreen3')
        canvas.create_text(mode.width//2, mode.height//10, 
        text='Welcome to Flappy Food Chain!', font=font)
        canvas.create_text(mode.width/2, 2*(mode.height//10), 
        text='"A very primitive twist on Agar.io with a bird."', 
        font='Arial 12')
        canvas.create_text(mode.width/2, 3*(mode.height//10), 
        text='Your goal: help Flappy devour 30 Food Blobs. ', 
        font = 'PeachPuff 25 ')
        canvas.create_text(mode.width/2, 4*(mode.height//10), 
        text='Oh, and watch out for the fox.', font = 'PeachPuff 25 ')
        canvas.create_text(mode.width/2, 5*(mode.height//10), 
        text='And the obstacles. ', font = 'PeachPuff 25 ')
        canvas.create_text(mode.width/2, 6*(mode.height//10), 
        text='And do it all in under 15 seconds :)', font = 'PeachPuff 25 ')
        canvas.create_text(mode.width/2, 7*(mode.height//10), 

        text='don' + '\'' + 't lose lol', font='Arial 50', fill = 'red')
        canvas.create_text(mode.width/2, 9*(mode.height//10), 
        text='Press any key to begin the game!', font='Arial 40 bold', 
        fill = color)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)



# player (OOP thingy #1)


class Player(Mode):
    def timerFired(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
        # new feature 10/28 --> you lose if you dont get enough pts in time

    def __init__(self, mode):
        self.mode = mode
        self.playerX = self.mode.app.width // 2
        self.playerY = self.mode.app.height // 2
        self.change = 15
        self.scrollX = 0
        self.scrollMargin = 50

        url = 'https://www.trzcacak.rs/myfile/full/441-4411625_' + \
        'parrot-sprite-sheet-bird-transparency.png'
        spritestrip = self.mode.app.loadImage(url) 

        self.sprites = [ ]
        for j in range(2):
            for i in range(3):
                sprite0 = spritestrip.crop((342*i, 0+300*j, 342+342*i, 
                265+300*j))
                sprite = self.mode.app.scaleImage(sprite0, 1/3)
                self.sprites.append(sprite)
        self.spriteCounter = 0

    def __hash__(self):
        return hash(self.playerX,)
    def __eq__(self, other):
        return (self.playerX == other.playerX)

    def makePlayerVisible(self):
            # scroll to make player visible as needed
            if (self.playerX < self.scrollX + self.scrollMargin): 
                self.scrollX = self.playerX - self.scrollMargin
            if (self.playerX > self.scrollX + self.mode.width - \
            self.scrollMargin): 
                self.scrollX = self.playerX - self.mode.width + \
                self.scrollMargin


    def move(self, dir):
        if dir == 'Left': 
            self.playerX -= self.change
            self.mode.scrollX -= self.change
        elif dir == 'Right': 
            self.playerX += self.change
            self.mode.scrollX += self.change
        elif dir == 'Up': 
            self.playerY -= self.change
        elif dir == 'Down': 
            self.playerY += self.change
        self.getBlobs()


    def getBlobs(self):  
        goodBlobs = []
        for blob in self.mode.blobs:
            if not blob.overlaps(self.playerX, self.playerY):
                goodBlobs.append(blob)
            else:
                self.mode.score += blob.value
                #increase the score^
        if self.mode.score > 30:
            self.mode.app.setActiveMode(self.mode.app.winMode)
        self.mode.blobs = goodBlobs
        


    def draw(self, canvas):
        drawX = self.playerX - self.mode.scrollX
        drawY = self.playerY
        # canvas.create_rectangle(drawX-self.radius, drawY-self.radius,
        #                        drawX+self.radius, drawY+self.radius,
        # fill='purple')
        # canvas.create_image(drawX - width //2, drawY- height//2, )
        sprite = self.sprites[self.spriteCounter]
        canvas.create_image(drawX, drawY, image=ImageTk.PhotoImage(sprite))


class Enemy(object): 
    def timerFired(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)

    def __init__(self, mode):
        self.mode = mode
        self.playerX = self.mode.app.width 
        self.playerY = random.randint(75, self.mode.app.height // 2)
        self.change = 15
        self.scrollX = 0
        self.scrollMargin = 50
        self.mode.distCount = 0

        url = 'https://d3tv7e6jdw6zbr.cloudfront.net/items/2012-12-06/' + \
        'npc_fox_fox_orangeFox_x1_walk_png_1354839598.png'
        spritestrip = self.mode.app.loadImage(url) 
        self.sprites = [ ]
        for i in range(3):
            sprite = spritestrip.crop((150*i, 0, 150+150*i, 135))
            self.sprites.append(sprite)
        self.spriteCounter = 0

    def makePlayerVisible(self):
            # scroll to make player visible as needed
            if (self.playerX < self.scrollX + self.scrollMargin): 
                self.scrollX = self.playerX - self.scrollMargin
            if (self.playerX > self.scrollX + self.mode.width - 
            self.scrollMargin): 
                self.scrollX = self.playerX - self.mode.width + \
                self.scrollMargin


    def move(self, dir):
        if dir == 'Left': 
            self.playerX -= self.change
            self.mode.scrollX -= self.change


    def draw(self, canvas):
        drawX = self.playerX - self.mode.scrollX - self.mode.distCount
        drawY = self.playerY
        self.mode.distCount += 10

        if (self.playerX - 50 > self.mode.width):
            self.move('Left')
        sprite = self.sprites[self.spriteCounter]
        canvas.create_image(drawX, drawY, image=ImageTk.PhotoImage(sprite))

class BirdGame(ModalApp): 
    def appStarted(app):
        app.winMode = WinMode()
        app.loseMode = loseMode()
        app.gameMode = GameMode()
        app.splashScreenMode = SplashScreenMode()
        app.setActiveMode(app.splashScreenMode)


class GameMode(Mode): 
    startTime = None
    elapsedTime = None
    secondsLeft = None
    endTime = None
    def appStarted(mode):
        GameMode.startTime = time.time()

        mode.locCursor = [-10, -10]
        mode.imgCursor = mode.scaleImage(
            mode.loadImage(
                'https://statici.behindthevoiceactors.com/'
                + 'behindthevoiceactors/_img/chars/daffy-duck-looney-'
                + 'tunes-duck-amuck-4.6.jpg'), 
                1/7)


        #player, enemy stuff
        mode.score = 0
        mode.scrollX = 0

        # set stuff 
        mode.player = Player(mode)
        mode.playerSet = set([mode.player])
        '''set dict thing^'''
        mode.enemy = Enemy(mode)
        mode.enemySet = set([mode.enemy]) 
        '''set dict thing^'''

        mode.blobs = []
        mode.blobSet = set()
        mode.maxX = 3000
        mode.blobDragged = None
        newBlob = None
        for i in range(100):
            randNum = random.randint(0, 30)
            if randNum <= 10 or 20 < randNum <= 29:
                newBlob = Food(
                    random.randint(0, mode.maxX),
                    random.randint(0, mode.height),
                    mode
                    )
            elif randNum <= 20:
                newBlob = medFood(
                    random.randint(0, mode.maxX),
                    random.randint(0, mode.height),
                    mode
                    )
            elif randNum == 30:
                newBlob = massiveFood(
                    random.randint(0, mode.maxX),
                    random.randint(0, mode.height),
                    mode
                    )
            mode.blobs.append(newBlob)
            mode.blobSet.add(newBlob)


    def keyPressed(mode, event):
        if event.key == 'S':
            print('''
            $$$$$$$$$$
            SUPERHELP:  
            $$$$$$$$$$


            Playing:
            ---------
            This side scrolling game consists of a Flappy (bird), its food, 
            and an enemy.
            The enemy is Fox, which will consistently move across the screen 
            from 
            right to left at random heights. 
            
            
            Losing:
            --------
            If you, Flappy, make direct contact with Fox--where direct contact 
            is defined by your middles meeting--you will die and thus LOSE the 
            game. 

            You will also lose if you, Flappy, don't eat 30 points worth of
            blobs in under 15 seconds.
            
            Winning:
            ---------
            The objective of the game is to eat
            enough food blobs to score more than 30 points. 

            Food blob values: 
            Small Blob (most common) --> 1 point
            Medium Blob (less common) --> 5 points
            Massive Blob (very rare) --> 15 points.

            Good luck, and happy flying!
            ''')
        mode.player.move(event.key)

    def mouseMoved(mode, event):
        mode.locCursor = [event.x, event.y]




    def mousePressed(mode, event):
        for blob in mode.blobs:
            if blob.overlaps(event.x + mode.scrollX, event.y): 
                #there is no mode.scrollY bc only worry about 1d so we good
                mode.blobDragged = blob
            
    def mouseReleased(mode, event):
        mode.blobDragged = None

    def mouseDragged(mode, event):
        if mode.blobDragged != None:
            mode.blobDragged.playerX = event.x + mode.scrollX
            mode.blobDragged.playerY = event.y 
            mode.player.getBlobs()
        
        mode.locCursor = [event.x, event.y]
    
    def timerFired(mode):
        # mode.timeCounter += 1
        mode.player.timerFired()
        mode.enemy.timerFired()


        if (mode.enemy.playerX - 50 == 0): #I THINK THIS IS THE KEY FOR SPAWNING
            mode.enemy = Enemy(mode)
        
        # new feature 10/28 --> you lose if you dont get enough pts in time
        if roundHalfUp(GameMode.endTime) == roundHalfUp(GameMode.startTime +
         15): 
            mode.app.setActiveMode(mode.app.loseMode) #you lose 
            GameMode.elapsedTime = roundHalfUp(GameMode.endTime 
            - GameMode.startTime)
            GameMode.secondsLeft = 15 - GameMode.elapsedTime

        if (mode.player.playerX == mode.enemy.playerX 
        and mode.player.playerY == mode.enemy.playerY):
            mode.app.setActiveMode(mode.app.loseMode) 
        

        # if playerSet in EnemySet:
        #     mode.app.setActiveMode(mode.app.loseMode)


    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill='SkyBlue1') 
        #create sky background

        canvas.create_image(mode.locCursor[0], mode.locCursor[1], 
        image=ImageTk.PhotoImage(mode.imgCursor))
        #locCursor LINE

        mode.player.draw(canvas)
        mode.enemy.draw(canvas)
        for blob in mode.blobs: 
            blob.draw(canvas)

        canvas.create_text(mode.width // 2, 30, 
        text='Score: ' + str(mode.score), font='Arial 30 bold')

        GameMode.endTime = time.time()
        canvas.create_text(mode.width // 2, 70, 
        text='Time: ' + str(roundHalfUp(time.time() - GameMode.startTime)), 
        font='Arial 40 bold')

        

class WinMode(Mode): 
    def redrawAll(mode, canvas):
        mode.colorList = ['dark khaki', 'IndianRed1', \
            'gray38', 'tomato', 'goldenrod']
        mode.color = mode.colorList[random.randint(0, len(mode.colorList)-1)]
        fontSize = random.randint(25, 30)
        yLocation = random.randint(50, mode.height - 50)

        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.color)
        canvas.create_text(mode.width // 2, yLocation, 
        text = "YOU DID IT YOU WON GOOD JOB GAME OVER",
        font = f'Helvetica {fontSize}')

        # canvas.create_text(mode.width // 2, yLocation+20, 
        # text = f"WITH {GameMode.secondsLeft} seconds left!",
        # font = f'Helvetica {fontSize}')
    
    def appStarted(mode):
        mode.app.timerDelay = 1000


class loseMode(Mode): 
    def redrawAll(mode, canvas):
        mode.color = 'gray38'
        fontSize = random.randint(25, 30)
        yLocation = random.randint(50, mode.height - 50)
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.color)
        
        canvas.create_text(mode.width // 2, yLocation, 
        text = "L you lost. press r to restart",
        font = f'Helvetica {fontSize}')

        # canvas.create_text(mode.width // 2, yLocation+20, 
        # text = f"If only you scored {50 - mode.score} more points...",
        # font = f'Helvetica {fontSize}')

    
    def appStarted(mode):
        mode.app.timerDelay = 1000
    
    def keyPressed(mode, event):
        if event.key == 'r':
            BirdGame(width=800, height=800)



class Food(object): 
    @staticmethod
    def distance(x1,y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5


    def __init__(self, cx, cy, mode):
        self.playerX = cx
        self.playerY = cy
        self.mode = mode
        self.value = 1

        # just for aesthetics (2 lines)
        self.colorList = ['yellow', 'lightblue', 'green', 'red']
        self.color = self.colorList[random.randint(0,3)]
        # end looks lol

        self.radius = 10 

    # def __hash__(self):
    #     return hash((self.playerX, self.playerY))
        
    def draw(self, canvas):
        drawX = self.playerX - self.mode.scrollX
        drawY = self.playerY
        canvas.create_oval(drawX-self.radius, drawY-self.radius,
                        drawX+self.radius, drawY+self.radius,fill=self.color)

    def overlaps(self, x, y):
        return Food.distance(self.playerX, self.playerY, x, y) < self.radius

class medFood(Food): 
    def __init__(self, cx, cy, mode):
        super().__init__(cx, cy, mode)
        self.value = 5
        self.radius = 15
        self.color = 'LemonChiffon2'

class massiveFood(Food): 
    def __init__(self, cx, cy, mode):
        super().__init__(cx, cy, mode)
        self.value = 15
        self.radius = 20
        self.color = 'dark orchid'

class Obstacle(Food):
    def __init__(self, cx, cy, mode):
        super().__init__(cx, cy, mode)
        self.colorList = ['salmon2', 'purple2']
        self.color = self.colorList[random.randint(0,len(self.colorList)-1)]



def runCreativeSidescroller():
    BirdGame(width=800, height=800)



#################################################
# testAll and main
#################################################

def testAll():
    print("Testing SideScroller...")
    runCreativeSidescroller()
    print("Done!")

def main():
    testAll()

if __name__ == '__main__':
    main()

