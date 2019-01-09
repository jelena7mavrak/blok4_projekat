from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Bullet(QLabel):
    def __init__(self,parent,x,y,pic):
        super(Bullet,self).__init__(parent)

        if(pic == '2674.png'):
            self.dimX = 20
            self.dimY = 20
        else:
            self.dimX = 10
            self.dimY = 15
