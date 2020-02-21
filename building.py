from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random

class Building(object):
    def __init__(self, mode):
        self.ratio = 1 / random.randrange(3, 6)
        self.image = mode.scaleImage(mode.buildingImage, self.ratio)
        self.width, self.height = self.image.size
        self.cx = mode.app.width + self.width / 2
        self.cy = mode.app.height - self.height / 2

    def getCoordinates(self):
        x0 = self.cx - self.width / 2
        y0 = self.cy - self.height / 2
        x1 = self.cx + self.width / 2
        y1 = self.cy + self.height / 2
        return x0, y0, x1, y1

    def move(self):
        self.cx -= 10

class GameMode(Mode):
    def appStarted(mode):
        mode.buildingImage = mode.loadImage('building1.png')
        mode.buildings = [ ]
        mode.timer = 0
        
    def createBuilding(mode):
        newBuilding = Building(mode)
        print(newBuilding.ratio)
        mode.buildings.append(newBuilding)

    def keyPressed(mode, event):
        if (event.key == 'c'):
            mode.createBuilding()
        #elif (event.key == 'Left'):
            #mode.moveBuilding()

    def moveBuilding(mode):
        for building in mode.buildings:
            building.move()

    def removeBuilding(mode):
        for building in mode.buildings:
            x0, y0, x1, y1 = building.getCoordinates()
            if (x1 < 0): mode.buildings.remove(building)

    def drawBuilding(mode, canvas):
        for building in mode.buildings:
            canvas.create_image(building.cx, building.cy, image = ImageTk.PhotoImage(building.image))

    def timerFired(mode):
        mode.moveBuilding()
        mode.removeBuilding()
        mode.timer += 100
        if (mode.timer % 2000 == 0):
            mode.createBuilding()
    
    def redrawAll(mode, canvas):
        mode.drawBuilding(canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 50

app = MyModalApp(width=500, height=500)