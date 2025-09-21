import webview
from pynput import mouse, keyboard
import time
import threading
import pygame
import tqdm

class App:
    def __init__(self):

        pygame.mixer.init()
        self.loadSounds()

        self.createWindow()
        self.detectMouseAndKeyboardMovement()

        self.soundThreadT = threading.Thread(target=self.soundThread, daemon=True, name="Sound Thread")
        self.soundThreadT.start()

    def loadSounds(self):

        self.beepSound = pygame.mixer.Sound("effectAlert.mp3")
        self.onStartsound = pygame.mixer.Sound("effectStart.mp3")

    def createWindow(self):
        self.isWindowActive = True
        self.buttonPressed = False
        self.timerDone = False
        self.window = webview.create_window("", html = self.readHtmlFile(), fullscreen=True, draggable=False, frameless=True, js_api=self, on_top=True)
        self.lastAction = time.time()
        self.onStartsound.play()
        self.window.events.closing += self.onWindowClosing

    def waitForNext(self):
        time.sleep(20*60)
        self.createWindow()

    def updateLastAction(self): 
        print(f"Detected action")
        self.lastAction = time.time()
    def onClick(self, x, y, button, pressed):    self.updateLastAction()
    def onMove(self,  x, y):    self.updateLastAction()
    def onPress(self,   key):   self.updateLastAction()
    def onRelease(self, key):   self.updateLastAction()
    def onWindowClosing(self):
        if self.timerDone == False:
            return False


    def detectMouseAndKeyboardMovement(self):

        self.mouseListener = mouse.Listener(on_move=self.onMove, on_click=self.onClick)
        self.keyboardListener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)

        print(f"begin yield")
        self.mouseListener.start()
        self.keyboardListener.start()
        print(f"end")

    def onButtonPress(self):
        if self.buttonPressed == True: return
        print(f"Button pressed")
        self.buttonPressed = True
        counter = 60
        while counter > 0:
            counter -= 1
            time.sleep(1)
            if time.time() - self.lastAction < 2:
                counter = 60
            self.window.evaluate_js(f"updateTimerOfDoom('{counter} seconds left')")
        self.timerDone = True
        if self.window == None: return
        self.isWindowActive = False
        self.window.destroy()

        
    


    def soundThread(self):

        while True:
            time.sleep(2)

            if self.isWindowActive == False: continue
            if self.buttonPressed == False:
                if time.time() - self.lastAction > 15: continue
            else:
                if time.time() - self.lastAction > 4: continue
            
            self.beepSound.play()


    def run(self):
        webview.start()

    def readHtmlFile(self):
        with open("index.html", "r") as f:
            return f.read()

while True:

    a = App()
    a.run()

    for x in tqdm.tqdm(range(20 * 60)):
        time.sleep(1)