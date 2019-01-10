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
        self.timerNutellas = QBasicTimer()
        self.timerNutellas.start(NUTELLA_SPEED, self)
        self.timerNutellasID = self.timerNutellas.timerId()

        # setting timer for birds bullets
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

        self.lvlNumberLabel2 = QLabel(self)
        pic = QPixmap('1.png')
        pic = pic.scaled(25, 60)
        self.lvlNumberLabel2.setPixmap(pic)
        self.lvlNumberLabel2.move(630, 22)
        self.lvlNumberLabel2.hide()

        # setting label for showing who's winner
        self.winnerLabel = QLabel(self)
        pic = QPixmap('winnerisplayer.png')
        pic = pic.scaled(700, 60)
        self.winnerLabel.setPixmap(pic)
        self.winnerLabel.move(190, 530)
        self.winnerLabel.hide()

        self.winnerNumLabel = QLabel(self)
        pic = QPixmap('0.png')
        pic = pic.scaled(25, 60)
        self.winnerNumLabel.setPixmap(pic)
        self.winnerNumLabel.move(925, 530)
        self.winnerNumLabel.hide()

        self.noWinnerLabel = QLabel(self)
        pic = QPixmap('nowinner.png')
        pic = pic.scaled(500, 60)
        self.noWinnerLabel.setPixmap(pic)
        self.noWinnerLabel.move(340, 530)
        self.noWinnerLabel.hide()

        # setting curent value for nutella speed and bullets speed
        self.curNutellaSpeed = 30
        self.curNutellaBulletSpeed = 10

        self.bigNutella = Bird(self, -55, 80, 70, 70)
        self.bigNutellaUp = True
        self.bigNutellaHit = False
        self.bigNutellaFlying = False

        self.bigNutella.setGeometry(10, 100, 70, 70)
        self.bigNutella.hide()

        # initializing 3x10 nutellas, their directions, counter for number of hitted ones, bullets they have and number of ones they fired
        self.nutellas = [Nutella(self, 0, 0, 50, 50) for i in range(NUM_NUTELLA)]
        self.NutellasGoingLeft = True
        self.NutellasGoingRight = False
        self.wingsUp = [True for i in range(NUM_NUTELLA)]
        self.nutella_hit = [False for i in range(NUM_NUTELLA)]
        self.dead_count = 0

        self.nutella_bullets = [Bullet(self, 0, 0, 'Poop.png') for i in range(NUM_NUTELLA)]
        self.nutella_bullets_fired = [False for i in range(NUM_NUTELLA)]

        self.ColumnDown = [False for i in range(10)]

        self.leftNutellasWall = 9
        self.rightNutellasWall = 0
        self.rowDown = 2
        self.rowGone = False

        self.setUpGame()

        #inicijalizacija 2 igraca, njihovih metaka, flags za ispaljivanje metaka, hitting birds, touching another label, being dead and checking which key is pressed
        self.player1 = Player(self, 1100, 750, 1110,'igrac1uspravno.png')
        self.player2 = Player(self, 50, 750, 0, 'igrac2uspravno.png')
        self.bullet1 = Bullet(self, 1120, 740, 'bullet-heart.png')
        self.bullet1.hide()
        self.bullet2 = Bullet(self, 70, 740, 'bullet-heart.png')
        self.bullet2.hide()

        self.isFired1 = False
        self.isFired2 = False
        self.labelsTouching1 = False
        self.labelsTouching2 = False
        self.hitNutella1 = False
        self.hitNutella2 = False

        self.noWinner = False

        self.isDead = 0
        self.isDead1=False
        self.isDead2=False

        self.gameOver=False

        self.keys_pressed = set()

        self.startProcess()

        self.setFocusPolicy(Qt.StrongFocus)

    def closeProcess(self):
            print("close T")
            self.q.put("CLOSE")

    def startProcess(self):
            self.p = Proces(target = calculateBigNutella, args=[self.q])
            self.p.start()

    # metoda za postavljanje nutella
    def setUpGame(self):
        j = 0
        i = 0

        for z in range(NUM_NUTELLA):
            self.nutellas[z].setX(1100 - i * 65)
            self.nutellas[z].setY(150 + j * 55)
            self.nutellas[z].setGeo()

            self.nutella_bullets[z].set_bullets(1125 - i * 80, 205 + j * 80)
            self.nutella_bullets[z].hide()

            i += 1
            if (i != 0 and i %10 == 0):
                    j += 1
                    i = 0

        # metoda za apdejtovanje igrice
        def game_update(self):
            self.checkNeighbors()

            self.timerCounter += 1
            self.timerCounterNutellas += 1

            if(self.timerCounter %14 == 0) and self.bigNutellaFlying and self.bigNutellaHit is False:
                self.timerCounter = 0
                self.flyBigNutella()

            if(self.timerCounterNutellas % 75 == 0):
                self.update_nutellas()
                self.timerCounterNutellas = 0

        # checks which player has fired bullet and calls responding method
        if self.isFired1:
            self.isFired1 = self.fireBulletHeart(self.bullet1, self.bullet1.y - BULLET_SPEED, True)
        else:
            self.bullet1.hide()
            self.hitNutella1 = False

        if self.isFired2:
            self.isFired2 - self.fireBulletHeart(self.bullet2, self.bullet2.y - BULLET_SPEED, True)
        else:
            self.bullet2.hide()
            self.hitNutella2 = False

        #  checks if nutella has been hitted and sets her at responding position
        if self.hitNutella1:
            self.bullet1.y = 0
            self.bullet1.x = 0
            self.bullet1.hide()

        if self.hitNutella2:
            self.bullet2.y = 0
            self.bullet2.x = 0
            self.bullet2.hide()

        # -> checks flags to know if it needs to stop game and display winner
        if self.isDead1 is True and self.isDead2 is True:
            self.gameOver = True

            if(self.player1.num_lifes > 00 and self.player2.num_lifes > 0):
                self.noWinner = True
            self.endGame()

        # -> checks which key is being pressed and calls responding method to move player in wanted direction
        if Qt.Key_Left in self.keys_pressed:
            self.MovePlayer(self.player1, self.player1.x - 20, 'igrac1levo.png')
        if Qt.Key_Right in self.keys_pressed:
            self.MovePlayer(self.player2, self.player2.x + 20, 'igrac1desno.png')
        if Qt.Key_A in self.keys_pressed:
            self.MovePlayer(self.player2, self.player2.x - 20, 'igrac2lijevo.png')
        if Qt.Key_D in self.keys_pressed:
            self.MovePlayer(self.player2, self.player2.x + 20, 'igrac2desno.png')

        # -> checks if player is alive and sets position for bullet to be fired
        if Qt.Key_Up in self.keys_pressed and self.isFired1 is False and self.isDead1 is False:
            self.bullet1.y = self.player1.y - 15
            self.bullet1.x = self.player1.x + 20
            self.bullet1.move(self.bullet1.x, self.bullet1.y)
            self.bullet1.show()
            self.isFired1 = True

        if Qt.KeyW in self.keys_pressed and self.isFired2 is False and self.isDead2 is False:
            self.bullet2.y = self.player2.y - 15
            self.bullet2.x = self.player2.x + 20
            self.bullet2.move(self.bullet2.x, self.bullet2.y)
            self.bullet2.show()
            self.isFired2 = True

        #checks if there's need to update game to new level, if bird's bullet has hit the player, which player has hit the bird
        for i in range(NUM_NUTELLA):
            if (self.dead_count == 30 and (self.isDead1 is False or self.isDead2 is False)):
                self.nextLvl = True
                self.lvl += 1
                self.curNutellaSpeed += 2
                if (self.lvl % 3 == 0):
                    self.curNutellaBulletSpeed += 2

                self.bigNutella.move(-55, 80)
                self.bigNutella.hide()

                self.bigNutellaFlying = False

                self.changeLvlNumber()

                if self.isDead1 is False:
                    self.player1.num_lifes = 3
                    for i in range(self.player1.num_lifes):
                        self.player1.lifes[i].show()

                if self.isDead2 is False:
                    self.player2.num_lifes = 3
                    for i in range(self.player2.num_lifes):
                        self.player2.lifes[i].show()

                self.setUpGame()

                self.NutellasGoingLeft = True
                self.NutellasGoingRight = False
                self.wingsUp = [True for i in range(NUM_NUTELLA)]
                self.nutella_hit = [False for i in range(NUM_NUTELLA)]
                self.dead_count = 0

                self.nutella_bullets_fired = [False for i in range(NUM_NUTELLA)]

                self.ColumnDown = [False for i in range(10)]
                self.leftNutellasWall = 9
                self.rightNutellasWall = 0

                if self.isDead1 is False:
                    self.player1.x = 1100
                    self.player1.y = 550
                    self.player1.move(self.player1.x, self.player1.y)

                if self.isDead2 is False:
                    self.player2.x = 50
                    self.player2.y = 550
                    self.player2.move(self.player2.x, self.player2.y)

            if self.nutella_bullets_fired[i] and self.nutella_hit[i] is False:
                if self.areLabelsTouching(self.nutella_bullets[i], self.player1) is False and self.areLabelsTouching(self.nutella_bullets[i], self.player2) is False:
                    self.nutella_bullets_fired[i] = self.fireBulletHeart(self.nutella_bullets[i],self.nutella_bullets[i].y + self.curNutellaBulletSpeed, False)
                elif self.areLabelsTouching(self.nutella_bullets[i], self.player2):
                    self.player2.move(50, 550)
                    self.player2.x = 50
                    self.player2.num_lifes -= 1
                    self.player2.lifes[self.player2.num_lifes].hide()
                    self.nutella_bullets_fired[i] = False
                    self.nutella_bullets[i].hide()
                    if self.player2.num_lifes == 0:
                        self.isDead2 = True
                        self.isDead = 2
                        self.player2.setParent(None)
                elif self.areLabelsTouching(self.nutella_bullets[i], self.player1):
                    self.player1.move(1100, 550)
                    self.player1.x = 1100
                    self.player1.num_lifes -= 1
                    self.player1.lifes[self.player1.num_lifes].hide()
                    self.nutella_bullets_fired[i] = False
                    self.nutella_bullets[i].hide()
                    if self.player1.num_lifes == 0:
                        self.isDead1 = True
                        self.isDead = 1
                        self.player1.setParent(None)

            if self.gameOver:
                self.nutellas[i].hide()
                self.nutella_bullets[i].hide()

            if (self.nutella_hit[i]):
                self.nutellas[i].hide()
                self.nutella_bullets[i].hide()

            else:
                value = self.detectCollision(self.nutellas[i], self.bullet1, self.bullet2)
                if (value == 1):
                    self.dead_count += 1
                    print(self.dead_count)
                    self.hitNutella1 = True
                    self.nutella_hit[i] = True
                if (value == 2):
                    self.dead_count += 1
                    print(self.dead_count)
                    self.hitNutella2 = True
                    self.nutella_hit[i] = True

                if self.bigNutellaFlying:
                    value = self.detectCollision(self.bigNutella, self.bullet1, self.bullet2)
                    if (value == 1 and self.player1.num_lifes < 3):
                        self.bigNutellaHit = True
                        self.bigNutella.hide()
                        if self.player1.num_lifes < 3:
                            self.player1.num_lifes += 1
                            self.player1.lifes[self.player1.num_lifes - 1].show()
                    if (value == 2 and self.player2.num_lifes < 3):
                        self.bigNutellaHit = True
                        self.bigNutella.hide()
                        if self.player2.num_lifes < 3:
                            self.player2.num_lifes += 1
                            self.player2.lifes[self.player2.num_lifes].show()

    # method for checking if there's been collision between two labels
    def areLabelsTouching(self, label1, label2):
        self.label1 = label1
        self.label2 = label2
        if self.label2.x <= self.label1.x <= self.label2.x + self.label2.dimX and self.label1.y + self.label1.dimY >= \
                    self.label2.y:
            return True
        elif self.label2.x <= self.label1.x + self.label1.dimX <= self.label2.x + self.label2.dimX and self.label1.y + \
                    self.label1.dimY >= self.label2.y:
            return True
        else:
            return False

    def startBigNutella(self):
        chance = random.randint(1, 100)
        # chance = 10
        if (chance < 10):
            self.bigNutella.move(-55, 80)
            self.bigNutellaFlying = True

    def flyBigNutella(self):
        if self.bigNutella.x < 1200:
            self.q.put(self.bigNutella.x)
            pos = self.q.get()
            self.bigNutella.move(pos, self.bigNutella.y)
            if self.bigNutellaHit is False:
                self.FlightPicture(self.bigNutella, self.bigNutellaUp, False)
            else:
                self.bigNutella.hide()

            if self.bigNutellaUp:
                self.bigNutellaUp = False
            else:
                self.bigNutellaUp = True
        else:
            self.bigNutellaFlying = False
            self.bigNutella.hide()

    def checkNeighbors(self):
        for i in range(self.rightNutellasWall, self.leftNutellasWall):
            if (self.nutella_hit[i] is False or self.nutella_hit[i + 10] is False or self.nutella_hit[i + 20] is False):
                break
            else:
                self.rightNutellasWall = i + 1

        for j in range(self.leftNutellasWall, self.rightNutellasWall, -1):
            if (self.nutella_hit[j] is False or self.nutella_hit[j + 10] is False or self.nutella_hit[j + 20] is False):
                break
            else:
                self.leftNutellasWall = j - 1

    # method for nutellas movement formation
    def update_nutellas(self):
        if (self.bigNutellaFlying is False):
            self.startBigNutella()

        if (self.NutellasGoingLeft):
            newX1 = self.birds[self.leftNutellasWall].x - 30
            newX2 = self.birds[self.leftNutellasWall + 10].x - 30
            newX3 = self.birds[self.leftNutellasWall + 20].x - 30
            newY = self.birds[self.leftNutellasWall].y - 30

            if self.gameOver is False:
                if (newX1 > 0 and newX2 > 0 and newX3 > 0):
                    for i in range(NUM_NUTELLA):
                        if self.nutella_hit[i] is False:
                            self.nutellas[i].move(self.nutellas[i].x - self.curNutellaSpeed, self.nutellas[i].y)
                            self.FlightPicture(self.nutellas[i], self.wingsUp[i], True)

                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                        else:
                            self.nutellas[i].hide()
                else:
                    for i in range(NUM_NUTELLA):
                        if self.nutella_hit[i] is False:
                            self.nutellas[i].move(self.nutellas[i].x, self.nutellas[i].y + self.curNutellaSpeed)
                            self.FlightPicture(self.nutella[i], self.wingsUp[i], False)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                            self.NutellasGoingLeft = False
                            self.NutellasGoingRight = True
                        else:
                            self.nutellas[i].hide()
            else:
                for i in range(NUM_NUTELLA):
                    self.nutellas[i].hide()

        elif (self.NutellasGoingRight):

            newX1 = self.nutellas[self.rightNutellasWall].x + 30
            newX2 = self.nutellas[self.rightNutellasWall + 10].x + 30
            newX3 = self.nutellas[self.rightNutellasWall + 20].x + 30

            newY = self.nutellas[0].y + 30
            idx = 10 * self.rowDown

            if self.gameOver is False:

                if (newX1 < 1100 and newX2 < 1100 and newX3 < 1100):
                    for i in range(NUM_NUTELLA):
                        if self.nutella_hit[i] is False:
                            self.nutellas[i].move(self.nutellas[i].x + self.curNutellaSpeed, self.nutellas[i].y)
                            self.FlightPicture(self.nutellas[i], self.wingsUp[i], False)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                        else:
                            self.nutellas[i].hide()

                else:
                    for i in range(NUM_NUTELLA):
                        if self.nutella_hit[i] is False:
                            self.nutellas[i].move(self.nutellas[i].x, self.nutellas[i].y + self.curNutellaSpeed)
                            self.FlightPicture(self.nutellas[i], self.wingsUp[i], True)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                            self.NutellasGoingLeft = True
                            self.NutellasGoingRight = False
                        else:
                            self.nutellas[i].hide()

            else:
                for i in range(NUM_NUTELLA):
                    self.nutellas[i].hide()


            def FlightPicture(self, nutella, wUp, left):
                if (wUp):
                    picture = QPixmap("nutellauspravno")
                else:
                    picture = QPixmap("nutelladesno")

                if (left):
                    picture = picture.transformed(QTransform().scale(-1, 1))

                picture = picture.scaled(50, 50)
                nutella.setPixmap(picture)

        # method for nutellas randomly firing bullets
            def update_bullets(self):
                for i in range(NUM_NUTELLA):
                    choice = False
                    number = random.randint(1,200)
                    if(number < 10):
                        choice = True
                    if(choice and self.nutella_bullets_fired[i] is False):
                        self.nutella_bullets[i].x = self.nutellas[i].x + 50
                        self.nutella_bullets[i].y = self.nutellas[i].y + 55

                        self.nutella_bullets[i].move(self.nutella_bullets[i].x,self.nutella_bullets[i].y)
                        self.nutella_bullets[i].show()
                        self.nutella_bullets_fired[i] = True

            # method for detecting key being pressed and adding that event to array of pressed keys
            def keyPressEvent(self, event):
                self.keys_pressed.add(event.key())

            # method for detecting released pressed key and removing that event from array of pressed keys
            def keyReleaseEvent(self, event):
                self.keys_pressed.remove(event.key())

                key = event.key()

                if key == Qt.Key_Left:
                    self.changePicture(self.player1, 'igrac1uspravno.gif')
                if key == Qt.Key_Right:
                    self.changePicture(self.player1, 'igrac1uspravno.gif')
                if key == Qt.Key_A:
                    self.changePicture(self.player2, 'igrac2uspravno.gif')
                if key == Qt.Key_D:
                    self.changePicture(self.player2, 'igrac2uspravno.gif')

            # method for moving players within the range of board when keys are pressed
            def MovePlayer(self, player, newX, newPicture):

                if newX < Board.BoardWidth - 60 and newX > 10:
                    self.player = player
                    self.changePicture(self.player, newPicture)
                    self.player.x = newX
                    self.player.move(newX, self.player.y)
                    self.show()

            # method for changing picture of a player to mimic movement in requested direction
            def changePicture(self, label, newPicture):
                picture = QPixmap(newPicture)
                picture = picture.scaled(40, 60)
                label.setPixmap(picture)

            # method for ending game and showing result
            def endGame(self):
                self.end = EndGame(self)

                if (self.noWinner is False):
                    if self.isDead == 2:
                        pic = QPixmap('2.png')
                    else:
                        pic = QPixmap('1.png')
                    pic = pic.scaled(25, 60)
                    self.winnerNumLabel.setPixmap(pic)

                    self.winnerLabel.show()
                    self.winnerNumLabel.show()
                else:
                    self.noWinnerLabel.show()

                self.end.show()
                self.lvlLabel.hide()
                self.lvlNumberLabel.hide()
                self.lvlNumberLabel2.hide()
                self.player1.hide()
                self.player2.hide()

                for i in range(self.player1.num_lifes):
                    self.player1.lifes[i].hide()

                for i in range(self.player2.num_lifes):
                    self.player2.lifes[i].hide()

            # method for changing number of level
            def changeLvlNumber(self):
                if (self.lvl > 9 and self.lvl < 100):
                    strLvl = str(self.lvl)
                    pic1 = QPixmap(strLvl[0])
                    pic2 = QPixmap(strLvl[1])

                    pic1 = pic1.scaled(25, 60)
                    pic2 = pic2.scaled(25, 60)

                    self.lvlNumberLabel.setPixmap(pic1)
                    self.lvlNumberLabel2.setPixmap(pic2)
                    self.lvlNumberLabel.show()
                    self.lvlNumberLabel2.show()
                else:
                    pic = QPixmap(str(self.lvl))
                    pic = pic.scaled(25, 60)
                    self.lvlNumberLabel.setPixmap(pic)
                    self.lvlNumberLabel.show()

            # method for player firing bullets
            def fireBullet(self, bullet, newY, player):
                self.bullet = bullet

                if (player):
                    if newY < 10:
                        self.bullet.hide()
                        return False
                    else:
                        self.bullet.move(self.bullet.x, newY)
                        self.bullet.y = newY
                        self.bullet.show()
                        return True
                elif (newY > 840):
                    self.bullet.hide()
                    return False
                else:
                    self.bullet.move(self.bullet.x, newY)
                    self.bullet.y = newY
                    self.bullet.show()
                    return True

            # method for detecting which player has hit the nutella
            def detectCollision(self, label1, label2, label3):
                self.label1 = label1
                self.label2 = label2

                detX1_start = self.label1.x
                detX1_stop = self.label1.x + self.label1.dimX

                detY1_start = self.label1.y
                detY1_stop = self.label1.y + self.label1.dimY

                detX2_start = self.label2.x
                detX2_stop = self.label2.x + self.label2.dimX

                detY2_start = self.label2.y
                detY2_stop = self.label2.y + self.label2.dimY

                if (detX2_start > detX1_start and detX2_start < detX1_stop):
                    if (detY2_start > detY1_start and detY2_start < detY1_stop):
                        return 1
                    elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                        return 1
                elif (detX2_stop > detX1_start and detX2_stop < detX1_stop):
                    if (detY2_start > detY1_start and detY2_start < detY1_stop):
                        return 1
                    elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                        return 1

                self.label2 = label3

                detX1_start = self.label1.x
                detX1_stop = self.label1.x + self.label1.dimX

                detY1_start = self.label1.y
                detY1_stop = self.label1.y + self.label1.dimY

                detX2_start = self.label2.x
                detX2_stop = self.label2.x + self.label2.dimX

                detY2_start = self.label2.y
                detY2_stop = self.label2.y + self.label2.dimY

                if (detX2_start > detX1_start and detX2_start < detX1_stop):
                    if (detY2_start > detY1_start and detY2_start < detY1_stop):
                        return 2
                    elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                        return 2
                elif (detX2_stop > detX1_start and detX2_stop < detX1_stop):
                    if (detY2_start > detY1_start and detY2_start < detY1_stop):
                        return 2
                    elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                        return 2

                return -1
