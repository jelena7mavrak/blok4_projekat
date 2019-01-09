from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Nutella(QLabel):
    def __init__(self, parent, x,y,dimX,dimY):
        super(Nutella, self).__init__(parent)

        #nutellas look, size and position on board
        nutella = QPixmap('')
        nutella = nutella.scaled(dimX,dimY)
        self.setPixmap(nutella)
        self.dimX = dimX
        self.dimY = dimY
        self.x = x
        self.y = y

