from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPalette, QIcon, QPixmap, QTransform
from player import Player
from endGame import EndGame
from nutella import Nutella
from bullet import Bullet
from multiprocessing import Queue, Process, Lock, JoinableQueue
import random, time

NUM_NUTELLA = 30
NUTELLA_SPEED = 400
NUTELLA_BULLET_SPEED = 1400
BULLET_SPEED = 30
BIGNUTELLA_SPEED = 50

def calculateBigNutella(q):
    while(True):
        pos = q.get()
        if(pos == "CLOSE"):
            print("ASD")
            break
        move = pos + BIGNUTELLA_SPEED
        q.put(move)

class Board(QFrame):

    BoardWidth = 1200
    BoardHeight = 600

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.q = Queue()
        self.qB = Queue()

        # setting timer for players
        self.timer = QBasicTimer()
        self.timer.start(20, self)

        # setting timer for nutellas
        self.timerNutella_bullet = QBasicTimer()
        self.timerNutella_bullet.start(NUTELLA_BULLET_SPEED, self)
        self.timerNutella_bulletID = self.timerNutella_bullet.timerId()

        self.timerCounter = 0
        self.timerCounterNutellas = 0

        # counter for levels
        self.lvl = 1
        self.nextLvl = False

        # setting label for showing number of levels
        self.lvlLabel = QLabel(self)
        pic = QPixmap('level.png')
        pic = pic.scaled(125, 65)
        self.lvlLabel.setPixmap(pic)
        self.lvlLabel.move(450, 20)

        self.lvlNumberLabel = QLabel(self)
        self.changeLvlNumber()
        self.lvlNumberLabel.move(600, 22)
















