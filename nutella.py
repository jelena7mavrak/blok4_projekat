from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Nutella(QLabel):

    def __init__(self, parent, x, y, dimX, dimY):
        super(Nutella, self).__init__(parent)

        # nutellas look, size and position on board
        nutella = QPixmap('nutellauspravno.png')
        nutella = nutella.scaled(dimX, dimY)
        self.setPixmap(nutella)
        self.dimX = dimX
        self.dimY = dimY
        self.x = x
        self.y = y

    # setter for x and y position
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    # method for moving nutella
    def move(self, x, y):
        self.setX(x)
        self.setY(y)
        self.setGeo()

    # method for setting nutella on x and y position
    def setNutella(self, x, y):
        self.x = x
        self.y = y

    # method for fixing nutella on board
    def setGeo(self):
        self.setGeometry(self.x, self.y, self.dimX, self.dimY)
        self.show()


