from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPalette, QIcon, QPixmap, QTransform
from player import Player
from endGame import EndGame
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

