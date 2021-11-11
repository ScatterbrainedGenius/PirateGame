'''
Name(s): Halley Price
CSC 201
Programming Project 3

A game in which the player controls the movement of a pirate ship by clicking to the left or right of it,
and can fire cannonballs at sea serpents by pressing x. Shooting 20 serpents successfully is a win,
and letting a serpent touch the ship is a loss. Points are lost for every serpent that crosses the bottom
of the screen without getting shot.

Assistance:
    I gave and received no assistance on this project.
'''
from graphics import *
import time
import random
import math

SERPENT_SPEED = 5
CANNONBALL_SPEED = 7
SHIP_SPEED = 25
NUM_LOSE = 1
NUM_WIN = 20
STALL_TIME = 0.05

def distanceBetweenPoints(point1, point2):
    '''
    Calculates the distance between two points
    
    Params:
    point1 (Point): the first point
    point2 (Point): the second point
    
    Returns:
    the distance between the two points
    '''
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x)*(p1x - p2x) + (p1y - p2y) * (p1y - p2y))


def isCloseEnough(img1, serpentImg):
    '''
    Determines if the cannonball and serpent are close enough to say the cannonball shot the serpent,
    or if the ship and serpent are close enough to say the serpent attacked the ship.
    
    Params:
    img1 (Image): the image of one particular cannonball or  the ship
    serpentImg (Image): the image of one particular serpent
    
    Returns:
    True if distance between the center of the first image and the center of the serpent is less than a
    threshold to say the serpent was shot/attacked the ship. Otherwise, it returns False.
    '''
    threshold = img1.getWidth() * 0.5 + serpentImg.getWidth() * 0.5
    distance = distanceBetweenPoints(img1.getAnchor(), serpentImg.getAnchor())
    return distance < threshold

def moveCannonballs(cannonballImgList):
    '''
    moves each cannonball image in a list of cannonball images
    
    Params:
    cannonballImgList (list): a list of images of cannonballs that are currently falling
    '''
    for cannonball in cannonballImgList:
        cannonball.move(0, -CANNONBALL_SPEED)

def moveSerpents(serpentImgList):
    '''
    moves each serpent image in a list of serpent images
    
    Params:
    serpentImgList (list): a list of images of serpents that are currently falling
    '''
    for serpent in serpentImgList:
        serpent.move(0,SERPENT_SPEED)


def moveShip(win, shipImg):
    '''
    Use left/right arrow keys to move the ship left or right.
    When the key pressed is neither the left or right arrow, the
    ship does not move.
    
    Params:
    win (GraphWin): the window where the ship is drawn
    shipImg (Image): the image of the ship
    '''
            
    click = win.checkMouse()
    if click != None:
        coord = click.getX()
        mid = shipImg.getAnchor().getX()
        if mid >= coord:
            shipImg.move(-SHIP_SPEED,0)
        else:
            shipImg.move(SHIP_SPEED,0)


def addSerpentToWindow(win):
    '''
    Draws the serpent at a random location just above the top of the window
    
    Params:
    win (GraphWin): the window the serpent will be drawn in
    
    Returns:
    an Image object of the serpent which includes its initital location
    '''
    startX = random.randrange(75,610)
    startY = -40
    serpent = Image(Point(startX, startY), "serpent.gif")
    serpent.draw(win)
    return serpent

def addCannonballToWindow(win, shipImg):
    '''
    Draws the cannonball centered just above the ship
    
    Params:
    win (GraphWin): the window the cannonball will be drawn in
    shipImg (Image): the ship image
    
    Returns:
    an Image object of the cannonball which includes its initital location
    '''
    startX = shipImg.getAnchor().getX()
    startY = 485
    cannonball = Image(Point(startX, startY), "cannonball.gif")
    cannonball.draw(win)
    return cannonball


def gameLoop(win, ship):
    '''
    Loop continues to allow the serpents to fall, the ship to move,
    and the cannonballs to shoot until enough serpents escape
    or the ship shoots enough serpents to end the game.
    
    win (GraphWin): the window where game play takes place
    ship (Image): the ship image
    '''
    serpentList = []
    cannonballList = []
    touch = 0
    score = 0
    scoreLabel = Text(Point(500, 100), '0')
    scoreLabel.draw(win)
    
    while touch < NUM_LOSE and score < NUM_WIN:
        fire = win.checkKey()
        
        if random.randrange(100) < 4:
            newSerpent = addSerpentToWindow(win)
            serpentList.append(newSerpent)
        
        if fire == 'x':
            newCannonball = addCannonballToWindow(win, ship)
            cannonballList.append(newCannonball)
        
        moveSerpents(serpentList)
        moveShip(win,ship)
        moveCannonballs(cannonballList)
        
        for serpent in serpentList:
            if serpent.getAnchor().getY() > 700:
                serpent.undraw()
                serpentList.remove(serpent)
                score = score - 1
                scoreLabel.setText(str(score))
                
            if isCloseEnough(ship, serpent):
                ship.undraw()
                touch = touch + 1
            
            for cannonball in cannonballList:
                if isCloseEnough(cannonball, serpent):
                    serpent.undraw()
                    serpentList.remove(serpent)
                    cannonball.undraw()
                    cannonballList.remove(cannonball)
                    score = score + 1
                    scoreLabel.setText(str(score))
                    
                if cannonball.getAnchor().getY() < -10:
                    cannonball.undraw()
                    cannonballList.remove(cannonball)

        time.sleep(STALL_TIME)
    if touch >= NUM_LOSE:
        time.sleep(0.5)
        return 'loss'
        
    else:
        time.sleep(0.5)
        return 'victory'
        
def main():
    # setup the game
    
    win2 = GraphWin("Instructions", 650, 300)
    win2.setBackground('deepskyblue2')
    Text(Point(325, 30), 'Click to sail the ship.').draw(win2)
    Text(Point(325, 75), 'Press x to fire the cannons.').draw(win2)
    Text(Point(325, 120), "Don't let the sea serpents attack.").draw(win2)
    Text(Point(325, 165), '20 points to win.').draw(win2)
    Text(Point(325, 210), 'Set sail in:').draw(win2)
    
    timer = 5
    timerLabel = Text(Point(325, 255), '5').draw(win2)
    for n in range(5):
        time.sleep(1)
        timer = timer - 1
        timerLabel.setText(str(timer)) 
    
    win2.close()

    win = GraphWin("PIRATES!!!", 666,666)
    water = Image(Point(333, 333), "water.gif")
    water.draw(win)
    ship = Image(Point(333,580), "ship.gif")
    ship.draw(win)
    
    play = gameLoop(win, ship)
    if play == 'loss':
        water.undraw()
        water.draw(win)
        m1 = Text(Point(333, 310),"The sea serpents attacked.").draw(win)
        m2 = Text(Point(333, 355), "You lose!").draw(win)
        m1.setFill('red')
        m2.setFill('red')
        
    else:
        gold = Image(Point(333, 333), "gold.gif")
        gold.draw(win)
        topLeft = Point(50, 300)
        bottomRight = Point(616, 366)
        label = Rectangle(topLeft, bottomRight)
        label.setFill('gold')
        label.draw(win)
        winText = Text(Point(333, 333),f"You defeated the sea serpents!").draw(win)
        
    time.sleep(3)
    win.close()


if __name__ == "__main__":
    main()
