from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random
import time

class Building(object):
    speed = 3
    def __init__(self, mode):
        self.ratio = 1/random.randint(1,4)
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
        self.cx -= Building.speed

class Lightning(Building):
    def __init__(self, mode):
        super().__init__(mode)
        self.ratio = 1/random.randint(5,9)
        self.image = mode.image
        self.image2 = mode.scaleImage(self.image, self.ratio)
        self.image3 = mode.image3
        self.width2, self.height2 = self.image3.size
        self.width,self.height = self.image2.size
        self.ratio2 = self.height / self.height2
        self.image4 = mode.scaleImage(self.image3, self.ratio2)
        self.cx = mode.app.width + self.width/2
        self.cy = self.height/2
        self.spritestrip = [self.image2,self.image4]
        self.timer = 0
        self.index = 0
        




class GameMode(Mode):
    def appStarted(mode):
        mode.buildingImage = mode.loadImage('https://i.imgur.com/VqNri0T.png')
        mode.buildings = [ ]
        mode.timer = 0
        mode.lightning = [ ]
        mode.image = mode.loadImage('lightning.png')
        mode.image3 = mode.loadImage("lightning2.png")
        mode.heart=Heart(mode)
        mode.heartsToGet = [ ]
        mode.distanceApart = 0
        mode.frequency = 5000

        #mode.lightningImage = mode.loadImage('lightning.png')
        #mode.lightningImage = mode.scaleImage(mode.lightningImage, 1/7)
        
    def createBuilding(mode):
        newBuilding = Building(mode)
        newBuilding.cx += mode.distanceApart
        mode.buildings.append(newBuilding)
    
    def createLightning(mode):
        newLightning = Lightning(mode)
        newLightning.cx += mode.distanceApart
        mode.lightning.append(newLightning)

    def keyPressed(mode, event):
        if (event.key == 'c'):
            mode.createBuilding()
        #elif (event.key == 'Left'):
            #mode.moveBuilding()

    def moveBuilding(mode):
        for building in mode.buildings:
            building.move()

    def moveLightning(mode):
        for lightning in mode.lightning:
            lightning.move()

    def removeBuildingAndLightning(mode):
        for building in mode.buildings:
            x0, y0, x1, y1 = building.getCoordinates()
            if (x1 < 0): mode.buildings.remove(building)
        for lightning in mode.lightning:
            x0, y0, x1, y1 = lightning.getCoordinates()
            if (x1 < 0): mode.lightning.remove(lightning)

    def drawBuilding(mode, canvas):
        for building in mode.buildings:
            canvas.create_image(building.cx, building.cy, image = ImageTk.PhotoImage(building.image))

    def drawLightning(mode, canvas):
        for lightning in mode.lightning:
            #canvas.create_image(lightning.cx, lightning.cy, image = ImageTk.PhotoImage(lightning.image2))
            canvas.create_image(lightning.cx, lightning.cy, image = ImageTk.PhotoImage(lightning.spritestrip[lightning.index]))

    def timerFired(mode):
        mode.moveBuilding()
        mode.moveLightning()
        mode.removeBuildingAndLightning()
        mode.timer += 100
        for lightning in mode.lightning:
            lightning.timer += 100
            if lightning.timer % 2000:
                lightning.index += 1
                lightning.index = lightning.index % len(lightning.spritestrip)
        if (mode.timer % mode.frequency == 0):
            mode.distanceApart = random.randrange(-40,40)
            probabilityOfLightning = random.randint(0,10)
            if probabilityOfLightning <= 5:
                mode.createLightning()
            else:
                mode.createBuilding()
        if (mode.timer % 5000 == 0):
            Building.speed += 1
            if (Building.speed > 40):
                Building.speed = 40
            mode.frequency -= 100
            if (mode.frequency < 2000):
                mode.frequency = 2000
            print(Building.speed, mode.frequency)
            
        # if mode.timer % 1500 == 0:
        #     newHeart = HeartToGet()
        #     mode.heartsToGet.append(newHeart)
    
    def redrawAll(mode, canvas):
        mode.drawBuilding(canvas)
        mode.drawLightning(canvas)
        mode.heart.draw(canvas)

class HeartToGet(Building):
    def __init__(self,mode):
        super().__init__(mode)
        self.image = mode.scaleImage(mode.heart, self.ratio)
        self.width, self.height = self.image.size
        self.cx = mode.app.width + self.width / 2
        self.cy = mode.app.height - self.height / 2


class Heart(object):
    def __init__(self,mode):
        self.mode=mode
        # self.x=x
        # self.y=y
        self.lives=3
        heartURL=('https://i.imgur.com/EqQDi3i.png')
        heart=self.mode.loadImage(heartURL)
        self.heart=self.mode.scaleImage(heart,1/30)

    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5

    #checks if the item contains the point
    def containsPoint(self,x,y):
        return self.distance(self.x,self.y,x,y)<25

    def heartCollide(self):
        heartsToKeep=[]
        for heart in self.mode.hearts:
            if heart.containsPoint(self.mode.playerX+self.mode.scrollX,
                                    self.y):
                self.lives+=1
            else:
                heartsToKeep.append(heart)
        self.mode.hearts=heartsToKeep
    
    #draws the heart that player can get 
    def draw(self,canvas):
        # drawX=self.x
        # drawY=self.y
        # canvas.create_image(drawX-self.mode.scrollX,drawY,
        # image=ImageTk.PhotoImage(self.heart))
        for i in range(self.lives):
            canvas.create_image(self.mode.app.width-(1+i)*50, 40,
        image=ImageTk.PhotoImage(self.heart))


class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 50

app = MyModalApp(width=500, height=500)