from Gameplay import *
from Vectors import *
import sys
from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtWidgets import QMainWindow,  QApplication, QPushButton,QDesktopWidget
from PyQt5.QtGui import QPainter, QImage, QColor, \
    QFont, QCursor, QPixmap, QIcon

class GameModel(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game = Game()
        path =  Game.get_config()
        self.prices = {
                       'castle' :
                           [self.game.config.get('Game','castle_1'),
                            self.game.config.get('Game','castle_2')] ,
                       'archers':
                           self.game.config.get( 'Archers', 'price'),
                       'poison':
                           self.game.config.get('Poison','price'),
                       'magic':
                           self.game.config.get('Magic','price')
                       }

        self.setWindowTitle('Tower Defence')
        self.load_images()
        self.red = QColor(255, 0, 0)
        self.green = QColor(0, 255, 0)
        self.blue = QColor(70, 165, 220)
        self.white = QColor(255, 255, 255)
        self.target = 'default'
        self.setCursor(self.cursors['default'])

        arch = QPushButton(self.icons['archers'], 'archers', self)
        arch.move(500, 0)
        arch.clicked.connect(lambda: self.on_button_click('archers'))

        mag = QPushButton(self.icons['mages'], 'mage', self)
        mag.move(600, 0)
        mag.clicked.connect(lambda: self.on_button_click('mages'))
        pois = QPushButton(self.icons['poison'], 'poison', self)
        pois.move(700, 0)
        pois.clicked.connect(lambda: self.on_button_click('poison'))

        upg_castle = QPushButton(self.icons['castle'], 'castle', self)
        upg_castle.move(800, 0)
        upg_castle.clicked.connect(lambda: self.game.upgrade_castle())

        upg_tow = QPushButton(self.icons['upgrade'], 'upgrade', self)
        upg_tow.move(900, 0)
        upg_tow.clicked.connect(lambda: self.game.upgrade_tower())

        storm = QPushButton(self.icons['storm'], 'storm', self)
        storm.move(300, 0)
        storm.clicked.connect(lambda: self.on_button_click('Thunderstorm'))

        self.timer = QBasicTimer()
        self.timer.start(20, self)
        #self.images_resize()
        self.game.start_game()
        self.showFullScreen()


    def on_button_click(self, cursor):
        self.setCursor(self.cursors[cursor])
        self.target = cursor

    def load_images(self):
        self.images = {'background': [QImage(), QImage(), QImage()],
                       'road': QImage(),
                       'archers': [QImage(), QImage(), QImage()],
                       'Tree': [QImage(), QImage(), QImage()],
                       'arrow': QImage(),
                       'dragon_attack': [QImage(), QImage(), QImage(),
                                        QImage(), QImage(),
                                        QImage(), QImage()],
                       'Dragon': [QImage(), QImage(),
                                  QImage(), QImage(),
                                  QImage(), QImage(), QImage()],
                       'Golem': [QImage(), QImage(), QImage(),
                                    QImage(), QImage(),
                                    QImage(), QImage()],
                       'golem_attack': [QImage(), QImage(), QImage(),
                                        QImage(), QImage(),
                                        QImage(), QImage()],
                       'Skeleton': [QImage(), QImage(), QImage(),
                                    QImage(), QImage(),
                                    QImage(), QImage()],
                       'Thunderstorm': QImage(),
                       'mage': [QImage(), QImage(), QImage()],
                       'magic': QImage(),
                       'poisontw': [QImage(), QImage(), QImage()],
                       'poison': QImage(),
                       'castle': [QImage(), QImage(), QImage()]}
        self.cursors = {'default': QCursor(QPixmap('images/cursor_03.png')),
                        'archers': QCursor(QPixmap('images/icon3.png')),
                        'mages': QCursor(QPixmap('images/icon5.png')),
                        'upgrade': QCursor(QPixmap('images/icon4.png')),
                        'poison':  QCursor(QPixmap('images/icon6.png')),
                        'Thunderstorm': QCursor(QPixmap('images/storm.png'))
                        }
        self.icons = {'archers': QIcon(QPixmap('images/icon3.png')),
                      'mages': QIcon(QPixmap('images/icon5.png')),
                      'upgrade': QIcon(QPixmap('images/icon4.png')),
                      'poison': QIcon(QPixmap('images/icon6.png')),
                      'castle': QIcon(QPixmap('images/icon1.png')),
                      'storm' : QIcon(QPixmap('images/storm.png'))}
        self.images['arrow'].load('images/arrow.png')
        self.images['road'].load('images/road.jpg')
        self.images['poison'].load('images/poison.png')
        self.images['magic'].load('images/magic.png')
        self.images['Thunderstorm'].load('images/thunderstorm.png')
        for i in range(0, 3):
            self.images['archers'][i]\
                .load('images/archers{}.png'.format(str(i + 1)))
            self.images['mage'][i]\
                .load('images/mages{}.png'.format(str(i + 1)))
            self.images['poisontw'][i]\
                .load('images/poisontw{}.png'.format(str(i + 1)))
            self.images['castle'][i]\
                .load('images/castle{}.png'.format(str(i + 1)))
            self.images['Tree'][i]\
                .load('images/tree{}.png'.format(str(i + 1)))
            self.images['background'][i]\
                .load('images/back{}.jpg'.format(str(i + 1)))
        for i in range(0, 7):
            self.images['Dragon'][i]\
                .load('images/dragon2{}.png'.format(str(i + 1)))
            self.images['dragon_attack'][i]\
                .load('images/dragon{}.png'.format(str(i + 1)))
            self.images['Skeleton'][i]\
                .load('images/skeleton{}.png'.format(str(i + 1)))
            self.images['Golem'][i]\
                .load('images/golem_run{}.png'.format(str(i + 1)))
            self.images['golem_attack'][i] \
                .load('images/golem_attack{}.png'.format(str(i + 1)))

    def images_resize(self):
        geometry = QDesktopWidget.screenGeometry(QDesktopWidget())
        width = geometry.width()
        height = geometry.height()
        print(height)
        print(width)
        for image in self.images.keys():
            if isinstance(self.images[image], list):
                for i in range(len(self.images[image])):
                    wth = self.images[image][i].width()
                    hgt = self.images[image][i].height()
                    self.images[image][i] =  self.images[image][i].scaledToWidth((wth * width) / 1920)
                    self.images[image][i] =self.images[image][i].scaledToHeight((hgt * height) / 1080)
            else:
                wth = self.images[image].width()
                hgt = self.images[image].height()
                self.images[image] = self.images[image].scaledToWidth((wth * width) / 1920)
                self.images[image] = self.images[image].scaledToHeight((hgt * height) / 1080)

    def timerEvent(self, event):
        self.game.enemy_move()
        self.game.fight()
        if self.game.player.is_dead():
            self.timer.stop()
            self.close()
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_map(painter)
        for tower in self.game.player.towers:
            matrix = painter.transform()
            painter.translate(tower.location.X, tower.location.Y)
            pic = self.images[tower.image][tower.level]
            painter.drawImage(-pic.width()/2, -pic.height()/2, pic)
            painter.setTransform(matrix)
        for enemy in self.game.creatures:
            matrix = painter.transform()
            painter.translate(enemy.location.X, enemy.location.Y)
            pic = self.images[enemy.image][enemy.get_image()]
            painter.drawImage(-pic.width() / 2, -pic.height() / 2, pic)
            painter.fillRect(-pic.width() / 2, -pic.height() / 2 - 10,
                             pic.width(), 7, self.red)
            painter.fillRect(-pic.width() / 2, -pic.height() / 2 - 10,
                             pic.width() * enemy.heath_percents(),
                             7, self.green)
            painter.setTransform(matrix)
        for bullet in self.game.bullets:
            matrix = painter.transform()
            pic = self.images[bullet.image]
            angle = 90 + (bullet.direction * 180 / math.pi)
            painter.translate(bullet.location.X, bullet.location.Y)
            painter.rotate(angle)
            painter.drawImage(-pic.width()/2, -pic.height()/2, pic)
            painter.setTransform(matrix)

        painter.setFont(QFont('Decorative', 16))

        painter.fillRect(20, 40, 250, 20, self.white)
        painter.fillRect(20, 40, 250 * self.game.player.mana / 100, 20, self.blue)
        painter.setPen(QColor(0, 0, 255))
        painter.drawText(120, 58, 'Mana : {}'.format(self.game.player.mana))

        painter.setPen(self.red)
        painter.drawText(10, 20, 'Health: {}'.format(self.game.player.health))
        painter.setPen(QColor(255, 255, 0))
        painter.drawText(120, 20, 'Gold: {}'.format(self.game.player.gold))




        tower = self.game.tower
        if self.game.level < 2:
            painter.drawText(840, 50,
                             str(self.prices['castle'][self.game.level]) + '$')
        painter.drawText(740, 50, self.prices['poison'] + '$')
        painter.drawText(640, 50, self.prices['magic'] + '$')
        painter.drawText(540, 50, self.prices['archers'] + '$')
        if self.game.tower is not None:
            painter.drawText(940, 50, str(tower.upg_price) + '$')
            pic = self.images[tower.image][tower.level]
            painter.setPen(self.green)
            painter.drawRect(tower.location.X - pic.width() / 2,
                             tower.location.Y - pic.height() / 2,
                             pic.width(), pic.height())
        if self.game.spell is not None:
            if not self.game.spell.is_executed:
                pic = self.images[self.game.spell.image]
                painter.drawImage(0, 0, pic)
                self.game.spell.get_image()
        painter.end()

    def draw_map(self, painter):
        painter.drawImage(0, 0,
                          self.images['background'][self.game.game_level])
        count = len(self.game.road)
        for i in range(count - 1):
            vector = Vector(self.game.road[i].X, self.game.road[i].Y)
            difference = self.game.road[i + 1] - vector
            while difference.length > 50:
                painter.drawImage(vector.X, vector.Y, self.images['road'])
                width = self.images['road'].width()
                delta = Vector(math.cos(difference.angle) * width,
                               math.sin(difference.angle) * width)
                vector = vector + delta
                difference = self.game.road[i + 1] - vector
        castle = self.images['castle'][self.game.level]
        painter.drawImage(self.game.road[count - 1].X - castle.width() / 2,
                          self.game.road[count - 1].Y - castle.width() / 2,
                          castle)

    def mousePressEvent(self, QMouseEvent):
        vector = Vector(QMouseEvent.x(), QMouseEvent.y())
        if self.target == 'archers':
            self.game.player.build_tower(Archers(vector), self.game.road)
        elif self.target == 'mages':
            self.game.player.build_tower(Mage(vector), self.game.road)
        elif self.target == 'poison':
            self.game.player.build_tower(PoisonTower(vector), self.game.road)
        elif self.target == 'Thunderstorm':
            self.game.cast_spell('Thunderstorm', vector)
        elif self.target == 'default':
            for tower in self.game.player.towers:
                delta = Vector(self.images[tower.image]
                               [tower.level].width() / 2,
                               self.images[tower.image]
                               [tower.level].height() / 2).length
                if (tower.location - vector).length < delta:
                    self.game.tower = tower
                    break

        self.on_button_click('default')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameModel()
    sys.exit(app.exec_())
