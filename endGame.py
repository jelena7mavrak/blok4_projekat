from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class EndGame(QLabel):
    def __init__(self, parent):
        super(EndGame, self).__init__(parent)

        # end game label look
        picture = QPixmap('gameover.png')
        picture = picture.scaled(460, 350)
        self.setPixmap(picture)
        self.setGeometry(350, 190, 450, 350)