from cmu_112_graphics import *
import pyaudio
import aubio
import random
import time
import math


# from https://github.com/aubio/aubio/blob/master/python/demos/demo_pyaudio.py
# with slight edit
import pyaudio
import sys
import numpy as np
import aubio
import threading



from cmu_112_graphics import *
from tkinter import*
from PIL import Image
from PIL import Image, ImageOps



class Pillar(object):
    def __init__(self,mode):
        self.scrollX = 0
        self.mode = mode
        self.width = self.mode.app.width
        self.height = self.mode.app.height
        num = random.randint(self.height/2,5*self.height/6)
        self.y = num
        self.cx = self.width + self.width/20
        self.r = self.width/30
        url1 = "https://i.imgur.com/9bIyKp1.png"
        self.image1 = self.mode.loadImage(url1)

        



    def draw(self,canvas):
        for pillar in self.mode.pillars:
            if type(pillar) == UpperPillar:
                x1,y1,x2,y2 = pillar.cx-pillar.r,0,pillar.cx+pillar.r,pillar.y
                canvas.create_rectangle(x1,y1,x2,y2,fill="green")
            else:
                x1,y1,x2,y2 = pillar.cx-pillar.r,pillar.y,pillar.cx+pillar.r,self.mode.app.height
                canvas.create_rectangle(x1,y1,x2,y2,fill="green")



class UpperPillar(Pillar):
    def __init__(self,mode):
        super().__init__(mode)
        num = random.randint(self.height/6,self.height/2)
        self.y = num

           


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

class GameMode(Mode):
    def appStarted(mode):
        # (mode.boundy0,mode.boundy1)=(mode.height*.7,mode.height)
        # (mode.boundx0,mode.boundx1)=(mode.scrollMargin*27,mode.width*3.5)
        # mode.cursor=[-1,-1]
        # mode.cacti={}
        # mode.lives=3
        # #creates enemy cactus in cacti dictionary
        # for i in range(15):
        #     randomX=random.randint(mode.boundx0,mode.boundx1)
        #     #randomX=900
        #     randomY=random.randint(mode.boundy0,mode.boundy1)
        #     mode.cacti[(EnemyCactus(mode,randomX,randomY))]=(randomX,randomY
        mode.heart=Heart(mode)
        mode.pillar = Pillar(mode)
        mode.pillars = []
        mode.pillars.append(mode.pillar)
        mode.pillar = Pillar(mode)
        mode.time = 0


        
    def redrawAll(mode,canvas):
        mode.heart.draw(canvas)
        
        for pillar in mode.pillars:
            pillar.cx -= pillar.scrollX 
            pillar.draw(canvas)
        


    def timerFired(mode):
        mode.time += 1
        #print("time = ",mode.time)
        if mode.time % 20 == 0:
            for pillar in mode.pillars:
                pillar.scrollX += 1
                if pillar.cx <= 0:
                    mode.pillars.pop(0)
        if mode.time % 60 == 0:
            probabilityOfUpperPillar = random.randint(0,10)
            if probabilityOfUpperPillar <= 5:
                newPillar = UpperPillar(mode)
            else:
                newPillar = Pillar(mode)
            mode.pillars.append(newPillar)



        





class SplashScreenMode(Mode):
    def appStarted(mode):
        urlStartScreen='https://i.imgur.com/psVcn8I.png'
        mode.bkground1=mode.loadImage(urlStartScreen)
        mode.snakeIdle='https://i.imgur.com/y6rR0MG.png'
        spritestrip=mode.loadImage(mode.snakeIdle)
        spritestrip1=mode.scaleImage(spritestrip,3)
        mode.sprites=[]
        #Creates moving sprite images
        for i in range(10):
                sprite = spritestrip1.crop(((0+31.8*i)*3, 3*10, 
                                            3*(31+31.8*i), 3*48))
                mode.sprites.append(sprite)
        mode.spriteCounter=0
    def timerFired(mode):
        mode.spriteCounter = ((1 + mode.spriteCounter) % len(mode.sprites))
    #draws snake and background
    def redrawAll(mode, canvas):
        canvas.create_image(300, 300,image=ImageTk.PhotoImage(mode.bkground1))
        #draw sprite
        sprite = mode.sprites[mode.spriteCounter]
        #cannot move above a y of 450, (25,450)
        canvas.create_image(300, 500,
        image=ImageTk.PhotoImage(sprite))
    #if any key is pressed the game starts
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
#help mode gives user help on the game
class HelpMode(Mode):
    def appStarted(mode):
        url='https://i.imgur.com/wDuVMcy.png'
        mode.bkground1=mode.loadImage(url)
        bkground2=mode.scaleImage(mode.bkground1,2/3)
    #draws background
    def redrawAll(mode, canvas):
        canvas.create_image(300, 300,
            image=ImageTk.PhotoImage(mode.bkground1))
    #if any key is pressed the game starts
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
#holds all the game functions
class MyModalApp(ModalApp):
    def appStarted(app):
        #app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        #app.helpMode = HelpMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 50
 
def runCreativeSideScroller():
    MyModalApp(width=600,height=600)
runCreativeSideScroller()




