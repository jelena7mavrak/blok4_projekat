from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Player(QLabel):

    def __init__(self, parent, x, y, x1, pic):
        super(Player, self).__init__(parent)

        # players look, size and position on board
        self.dimX = 40
        self.dimY = 60
        player = QPixmap(pic)
        player = player.scaled(self.dimX, self.dimY)
        self.setPixmap(player)
        self.x = x
        self.y = y
        self.setGeometry(x, y, self.dimX, self.dimY)

        # number of lives and fixing them on board
        self.num_lifes = 3
        self.lifes = [QLabel(parent) for i in range(self.num_lifes)]
        life = QPixmap(pic)
        life = life.scaled(30, 40)

        for i in range(self.num_lifes):
            self.lifes[i].setPixmap(life)
            self.lifes[i].setGeometry(x1, 10, 30, 40)
            self.lifes[i].show()
            x1 += 30
