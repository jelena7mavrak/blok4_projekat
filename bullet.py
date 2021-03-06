from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Bullet(QLabel):
    def __init__(self,parent,x,y,pic):
        super(Bullet,self).__init__(parent)

        if(pic == 'bullet-heart.png'):
            self.dimX = 20
            self.dimY = 20
        else:
            self.dimX = 19
            self.dimY = 19
        #izgled metka, velicina i pozicija na pozadini
        bullet = QPixmap(pic)
        bullet = bullet.scaled(self.dimX,self.dimY)
        self.setPixmap(bullet)
        self.x = x
        self.y = y
        self.setGeometry(x,y,self.dimX,self.dimY)

    #setter za x i y poziciju
    def set_bullets(self,x,y):
        self.x = x
        self.y = y
        self.setGeometry(x,y,self.dimX,self.dimY)
