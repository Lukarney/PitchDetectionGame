from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random
import pyaudio
import sys
import numpy as np
import aubio

# from https://github.com/aubio/aubio/blob/master/python/demos/demo_pyaudio.py
# with slight edit
# initialise pyaudio
p = pyaudio.PyAudio()
# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 9000
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)
if len(sys.argv) > 1:
    # record 5 seconds
    output_filename = sys.argv[1]
    record_duration = 1 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run forever
    outputsink = None
    record_duration = None
# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

class Building(object):
    speed = 3
    def __init__(self, mode):
        self.mode = mode
        self.ratio = 1 / random.randrange(1, 4)
        self.image = mode.scaleImage(mode.buildingImage, self.ratio)
        self.width, self.height = self.image.size
        self.cx = mode.app.width + self.width / 2
        self.cy = mode.app.height - self.height / 2
    def collision(self):
        if abs(self.cx - self.mode.app.gameMode.player.x) < self.width/2 + 20\
        and abs(self.cy - self.mode.app.gameMode.player.y) < self.height/2 + 20:
            self.mode.gameOver = True
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
        
class Background(object):

    def __init__(self, cx, scrollX):

        self.scrollX = scrollX

        self.cx = cx

class Heart(object):

    def __init__(self,mode):

        self.mode=mode

        heartURL=('https://i.imgur.com/EqQDi3i.png')

        heart=self.mode.loadImage(heartURL)

        self.heart=self.mode.scaleImage(heart,1/30)


    #draws the heart that player can get 
    def draw(self,canvas):

        for i in range(self.mode.app.gameMode.player.lives):

            canvas.create_image(self.mode.app.width-(1+i)*50, 40,

        image=ImageTk.PhotoImage(self.heart))

# player always stays at one spot
class Player(object):
    # player starts off in the center of the screen and has lives
    def __init__(self,mode):
        self.mode = mode
        self.lives = 3
        self.x = self.mode.app.width/4
        self.y = self.mode.app.height/2
        # fire ball sprite animation
        url = 'https://i.imgur.com/OQO873E.png'
        spritestrip = mode.loadImage(url)
        self.sprites = [ ]
        cropx, cropy = 660, 114
        cropx = cropx / 6
        for i in range(6):
            sprite = spritestrip.crop((cropx*i, 0, cropx*(i+1), cropy))
            scaleSprite = mode.scaleImage(sprite,1/2)
            self.sprites.append(scaleSprite)
        self.imageWidth, self.imageHeight = scaleSprite.size
        self.spriteCounter = 0
        self.timerDelay = 50
    # indexing through cropped images
    def timerFired(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
    # draw player animation
    def draw(self,canvas):
        sprite = self.sprites[self.spriteCounter]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))

class Arrow(object):
    # start at random y and right side of the screen, load arrow's image 
    def __init__(self,mode):
        self.mode = mode
        self.x = self.mode.app.width
        self.y = random.randint(50,self.mode.app.height-50)
        url = 'https://i.imgur.com/W6krzRL.png'
        self.image1 = self.mode.loadImage(url)
        self.image2 = self.mode.scaleImage(self.image1, 1/6)
        self.imageWidth, self.imageHeight = self.image2.size
    # move across the screen
    def timerFired(self):
        self.x -= 40
        if self.x < 0:
            self.x = self.mode.app.width
            self.y = random.randint(50,self.mode.app.height-50)
    # if collides with player, player.lives -1
    def collision(self):
        if abs(self.x - self.mode.app.gameMode.player.x) < 17\
        and abs(self.y - self.mode.app.gameMode.player.y) < 20:
            self.mode.app.gameMode.player.lives -= 1
    # draw arrow
    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.image2))

# Start Menu
class SplashScreenMode(Mode):
    def appStarted(mode):

        url='https://i.imgur.com/5WVj6QH.png'

        mode.bkground1=mode.loadImage(url)

        mode.bkground2=mode.scaleImage(mode.bkground1,1/4)

    def redrawAll(mode, canvas): 

        # background & name

        canvas.create_rectangle(0,0,mode.app.width,mode.app.height,

        fill = 'black')

        canvas.create_image(mode.app.width/2, mode.app.height/2,

            image=ImageTk.PhotoImage(mode.bkground2))

        # start button

        canvas.create_rectangle(mode.app.width/2 + 100, mode.app.height/2 + 20,
                                mode.app.width/2 - 100, mode.app.height/2 - 20,
                                outline = 'white')

        # instruction button

        canvas.create_rectangle(mode.app.width/2 + 100, mode.app.height/2 + 70 + 20,
                                mode.app.width/2 - 100, mode.app.height/2 + 70 - 20,
                                outline = 'white')

        # start text

        canvas.create_text(mode.app.width/2,mode.app.height/2,\
                            text='Start',font='Arial 20 bold',fill='white')

        # instruction text

        canvas.create_text(mode.app.width/2,mode.app.height/2 + 70,\
                            text='Instruction',font='Arial 20 bold',fill='white')

    # press key to go to different modes

    def mousePressed(mode, event):

        if mode.app.width/2 - 100 < event.x < mode.app.width/2 + 100 and \
            mode.app.height/2 - 20 < event.y < mode.app.height/2 + 20:
            mode.app.setActiveMode(mode.app.gameMode)

        elif mode.app.width/2 - 100 < event.x < mode.app.width/2 + 100 and \
            mode.app.height/2 + 70 - 20 < event.y < mode.app.height/2 + 70 + 20:
            mode.app.setActiveMode(mode.app.helpMode)


# actual gaming
class GameMode(Mode):
    # set up game state
    def appStarted(mode):
        mode.player = Player(mode)
        mode.arrow = Arrow(mode)
        mode.heart = Heart(mode)
        mode.gameOver = False
        mode.time = 0
        mode.distanceApart = 0
        mode.frequency = 5000
        # obstacles
        mode.buildingImage = mode.loadImage('https://i.imgur.com/VqNri0T.png')
        mode.buildings = [ ]
        mode.timer = 0
        mode.lightning = [ ]
        mode.image = mode.loadImage('https://i.imgur.com/krNzgqy.png')
        mode.image3 = mode.loadImage("https://i.imgur.com/nwky2GO.png")
        # background
        mode.cx = mode.app.width / 2
        mode.cy = mode.app.height / 2
        mode.loadBackground()
        mode.background1 = Background(3 * mode.backgroundWidth / 2, -mode.backgroundWidth)
        mode.background2 = Background(3 * mode.backgroundWidth / 2, 0)
        gameOverUrl = 'https://i.imgur.com/jbqJvTX.png'
        mode.bkground1=mode.loadImage(gameOverUrl)
        mode.bkground2=mode.scaleImage(mode.bkground1,1/4)
        mode.time=0

    def keyPressed(mode,event):
        if mode.gameOver==True:
            if event.key=="Space":
                mode.appStarted()
                

    def loadBackground(mode):
        url = 'https://i.imgur.com/rcVRsPw.jpg'
        mode.backgroundImage = mode.loadImage(url)
        mode.backgroundWidth, mode.backgroundHeight = mode.backgroundImage.size
        mode.resizeRatio = (mode.app.height + 2) / mode.backgroundHeight
        mode.backgroundImage = mode.scaleImage(mode.backgroundImage, mode.resizeRatio)
        mode.backgroundWidth, mode.backgroundHeight = mode.backgroundImage.size
        mode.backgroundSpeed = mode.app.height / 50

    def createBuilding(mode):
        newBuilding = Building(mode)
        mode.buildings.append(newBuilding)

    def createLightning(mode):
        newLightning = Lightning(mode)
        mode.lightning.append(newLightning)

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
        if mode.gameOver == False:
            mode.time += .1
        # Pitch controlling
        audiobuffer = stream.read(buffer_size)
        signal = np.fromstring(audiobuffer, dtype=np.float32)
        pitch = pitch_o(signal)[0]
        if 40 < pitch < 50: 
            mode.player.y += 20
        elif 50 < pitch < 60: 
            mode.player.y += 10
        elif 70 > pitch > 60: 
            mode.player.y -= 10
        elif pitch > 70:
            mode.player.y -= 20
        # make player visible 
        playerSize = 25
        if mode.player.y + playerSize >= mode.app.height:
            mode.player.y = mode.app.height - playerSize
        elif mode.player.y - playerSize <= 0:
                mode.player.y = playerSize
        # check collision
        for building in mode.buildings:
            building.collision()
        for lightning in mode.lightning:
            lightning.collision()
        mode.arrow.collision()
        if mode.player.lives == 0:
            mode.gameOver = True
        # background scroll
        mode.background1.scrollX += mode.backgroundSpeed
        mode.background2.scrollX += mode.backgroundSpeed
        mode.player.timerFired()
        mode.arrow.timerFired()
        # obstacles
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
        if (mode.timer % 500 == 0):
            Building.speed += 5
            if (Building.speed > 40):
                Building.speed = 40
            mode.frequency -= 100
            if (mode.frequency < 2000):
                mode.frequency = 2000

    def drawBackground1(mode, canvas):
        sx = mode.background1.scrollX % (2 * mode.backgroundWidth)
        canvas.create_image(mode.background1.cx - sx, mode.cy, image=ImageTk.PhotoImage(mode.backgroundImage))

    def drawBackground2(mode, canvas):
        sx = mode.background2.scrollX % (2 * mode.backgroundWidth)
        canvas.create_image(mode.background2.cx - sx, mode.cy, image=ImageTk.PhotoImage(mode.backgroundImage))
    
    def redrawAll(mode, canvas):
        # draw background
        mode.drawBackground1(canvas)
        mode.drawBackground2(canvas)
        # draw obstacles
        mode.drawBuilding(canvas)
        mode.drawLightning(canvas)
        # draw player
        mode.player.draw(canvas)
        # draw arrow
        mode.arrow.draw(canvas)
        # draw heart
        mode.heart.draw(canvas)
        if mode.gameOver==True:
            canvas.create_rectangle(0,0,mode.app.width,mode.app.height,fill='black')
            canvas.create_image(mode.app.width/2, mode.app.height/2, image=ImageTk.PhotoImage(mode.bkground2))
            canvas.create_text(mode.app.width/2 + 150, mode.app.height/2 - 50,text='Time: \n %0.1f seconds' % mode.time,
                                font='Arial 25 bold italic', fill='white')
            canvas.create_text(mode.app.width/2, mode.app.height - 100,text='Press Space to Restart',
                                font='Arial 25 bold italic', fill='white')

# Give Instructions
class HelpMode(Mode):
    def appStarted(mode):
        url='https://i.imgur.com/4SAC7E8.jpg'
        mode.bkground1=mode.loadImage(url)
        mode.bkground2=mode.scaleImage(mode.bkground1,2/3)
    def redrawAll(mode, canvas):
        canvas.create_image(mode.app.width/2, mode.app.height/2, image=ImageTk.PhotoImage(mode.bkground2))
    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.splashScreenMode)

# top level class calls GameMode, HelpMode, and SplashScreenMode
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

# Function that calls MyModalApp to run the game
def runCreativeSidescroller():
    MyModalApp(width=500,height=500)

runCreativeSidescroller()

