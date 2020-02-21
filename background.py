from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random

class Background(object):
    def __init__(self, cx, scrollX):
        self.scrollX = scrollX
        self.cx = cx

class GameMode(Mode):
    def appStarted(mode):
        mode.cx = mode.app.width / 2
        mode.cy = mode.app.height / 2

        mode.loadBackground()
        mode.background1 = Background(3 * mode.backgroundWidth / 2, -mode.backgroundWidth)
        mode.background2 = Background(3 * mode.backgroundWidth / 2, 0)
        
    def loadBackground(mode):
        mode.backgroundImage = mode.loadImage('background2.jpeg')
        mode.backgroundWidth, mode.backgroundHeight = mode.backgroundImage.size
        mode.resizeRatio = (mode.app.height + 2) / mode.backgroundHeight
        mode.backgroundImage = mode.scaleImage(mode.backgroundImage, mode.resizeRatio)
        mode.backgroundWidth, mode.backgroundHeight = mode.backgroundImage.size
        mode.backgroundSpeed = mode.app.width / 100

    def timerFired(mode):
        mode.background1.scrollX += mode.backgroundSpeed
        mode.background2.scrollX += mode.backgroundSpeed

    def drawBackground1(mode, canvas):
        sx = mode.background1.scrollX % (2 * mode.backgroundWidth)
        canvas.create_image(mode.background1.cx - sx, mode.cy, image=ImageTk.PhotoImage(mode.backgroundImage))

    def drawBackground2(mode, canvas):
        sx = mode.background2.scrollX % (2 * mode.backgroundWidth)
        canvas.create_image(mode.background2.cx - sx, mode.cy, image=ImageTk.PhotoImage(mode.backgroundImage))
        

    def redrawAll(mode, canvas):
        mode.drawBackground1(canvas)
        mode.drawBackground2(canvas)
        canvas.create_text(mode.cx, 50, text = f'{mode.backgroundWidth}, {mode.backgroundHeight}', fill = 'yellow')

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 50

app = MyModalApp(width=500, height=500)