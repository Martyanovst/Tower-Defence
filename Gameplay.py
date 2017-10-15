from Vectors import Vector
import math
import threading
import time
import config
import os


class Game:
    def __init__(self):
        path = Game.conf()
        config.create_config(path)
        self.config = config.get_config(path)
        self.bullets = []
        self.road = ([Vector(0, 350), Vector(1000, 350)],)
        self.player = Player()
        self.level = 0
        self.tower = None
        self.game_level = 0
        self.monsters = []
        self.lock = threading.Lock()
        self.spawn = threading.Thread(target=self.create)
        self.spell = None

    def start_game(self):
        self.spawn.start()

    @staticmethod
    def conf():
        return os.getcwd() + '\Config.ini'

    def cast_spell(self, class_, location):
        mana_cost = int(self.config.get(class_, 'mana'))
        if self.player.mana >= mana_cost:
            self.player.mana -= mana_cost
            self.spell = Spell(class_, self)
            self.spell.invoke(self.monsters, location)

    def create(self):
        self.first_level()
        self.second_level()
        self.third_level()
        self.fourth_level()
        self.fifth_level()

    def first_level(self):
        tree = 'Tree'
        skeleton = 'Skeleton'
        dragon = 'Dragon'
        time.sleep(7)
        for i in range(4):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(1)
        self.monsters.append(Monster(self.road[0], tree))
        time.sleep(0.5)
        self.monsters.append(Monster(self.road[0], tree))
        time.sleep(0.5)
        self.monsters.append(Monster(self.road[0], skeleton))
        for i in range(6):
            self.monsters.append(Monster(self.road[0], tree))
            time.sleep(0.5)
            self.monsters.append(Monster(self.road[0], skeleton))
            time.sleep(1)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[0], dragon))
        self.lock.release()

    def second_level(self):
        while len(self.monsters) != 0:
            time.sleep(1)
        self.change_level(([Vector(0, 200), Vector(400, 200),
                            Vector(400, 500), Vector(1000, 500)],))
        tree = 'Tree'
        skeleton = 'Skeleton'
        golem = 'Golem'
        time.sleep(7)
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], tree))
            self.lock.release()
            time.sleep(0.5)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(1)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[0], golem))
        self.lock.release()
        time.sleep(5)
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], tree))
            self.lock.release()
            time.sleep(1)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
        self.monsters.append(Boss(self.road[0], golem))

    def third_level(self):
        tree = 'Tree'
        skeleton = 'Skeleton'
        dragon = 'Dragon'
        golem = 'Golem'
        while len(self.monsters) != 0:
            time.sleep(1)
        self.change_level(([Vector(0, 600), Vector(1000, 600)],
                           [Vector(1000, 0), Vector(1000, 600)]))
        self.player.get_coins(100)
        time.sleep(10)
        for i in range(8):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], tree))
            self.lock.release()
        self.lock.acquire()
        self.monsters.append(Monster(self.road[0], tree))
        self.monsters.append(Monster(self.road[1], tree))
        self.lock.release()
        time.sleep(3)
        for i in range(6):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(1)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], skeleton))
            self.lock.release()
        for i in range(8):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(1)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], skeleton))
            self.lock.release()
        time.sleep(3)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[1], dragon))
        self.lock.release()
        while len(self.monsters) != 0:
            time.sleep(1)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[1], golem))
        self.monsters.append(Boss(self.road[0], golem))
        self.lock.release()

    def fourth_level(self):
        tree = 'Tree'
        skeleton = 'Skeleton'
        dragon = 'Dragon'
        golem = 'Golem'
        while len(self.monsters) != 0:
            time.sleep(1)
        self.change_level(([Vector(0, 700), Vector(1000, 700)],
                           [Vector(1000, 0), Vector(1000, 400),
                            Vector(520, 400), Vector(520, 700),
                            Vector(1000, 700)]))
        self.player.get_coins(100)
        time.sleep(10)
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(0.4)
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], skeleton))
            self.lock.release()
            time.sleep(0.4)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], tree))
            self.lock.release()
            time.sleep(0.8)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[0], dragon))
        self.lock.release()
        time.sleep(3)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[1], dragon))
        self.lock.release()
        time.sleep(5)
        self.monsters.append(Boss(self.road[1], golem))
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(0.2)
        for i in range(10):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], skeleton))
            self.lock.release()
            time.sleep(0.3)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], tree))
            self.lock.release()
            time.sleep(0.5)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[1], golem))
        self.monsters.append(Boss(self.road[0], golem))
        self.lock.release()

    def fifth_level(self):
        tree = 'Tree'
        skeleton = 'Skeleton'
        dragon = 'Dragon'
        golem = 'Golem'
        while len(self.monsters) != 0:
            time.sleep(1)
        self.change_level(([Vector(0, 700), Vector(220, 700),
                            Vector(220, 400), Vector(380, 400),
                            Vector(380, 700), Vector(1000, 700)],
                           [Vector(1000, 0), Vector(1000, 400),
                            Vector(520, 400), Vector(520, 700),
                            Vector(1000, 700)],
                           [Vector(0, 240), Vector(220, 240),
                            Vector(220, 400), Vector(380, 400),
                            Vector(380, 700), Vector(1000, 700)]))
        self.player.get_coins(250)
        time.sleep(15)
        for i in range(12):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], tree))
            self.lock.release()
            time.sleep(0.15)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], tree))
            self.lock.release()
            time.sleep(0.15)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[2], tree))
            self.lock.release()
            time.sleep(0.15)
        time.sleep(3)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[2], golem))
        self.monsters.append(Boss(self.road[1], dragon))
        self.lock.release()
        time.sleep(10)
        for i in range(12):
            self.lock.acquire()
            self.monsters.append(Monster(self.road[0], skeleton))
            self.lock.release()
            time.sleep(0.15)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[1], tree))
            self.lock.release()
            time.sleep(0.15)
            self.lock.acquire()
            self.monsters.append(Monster(self.road[2], skeleton))
            self.lock.release()
            time.sleep(0.15)
        time.sleep(7)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[0], golem))
        self.monsters.append(Boss(self.road[1], golem))
        self.lock.release()
        time.sleep(7)
        self.lock.acquire()
        self.monsters.append(Boss(self.road[2], golem))
        self.lock.release()

    def fight(self):
        for tower in self.player.towers:
            bullet = tower.fire(self.monsters)
            if bullet is not None:
                self.bullets.append(bullet)

    def enemy_move(self):
        self.lock.acquire()
        for enemy in self.monsters:
            enemy.move(self.player)
            if enemy.is_completed:
                self.monsters.remove(enemy)
        self.lock.release()
        for bullet in self.bullets:
            bullet.move()
        self.bullets = list(filter(lambda x: not x.hit, self.bullets))
        dead = list(filter(lambda x: x.is_dead(), self.monsters))
        self.monsters = list(filter(lambda x: not x.is_dead(), self.monsters))
        if self.player.mana < 100:
            self.player.mana += 2 * len(dead)
        self.lock.acquire()
        for e in dead:
            self.player.get_coins(e.price)
        self.lock.release()

    def change_level(self, next_path):
        self.bullets.clear()
        self.player.towers.clear()
        self.player.health = int(self.config.get('Player', 'health'))
        self.level = 0
        self.road = next_path
        self.player.gold += int(self.config.get('Player', 'level_reward'))
        self.tower = None
        self.game_level += 1

    def upgrade_tower(self):
        if self.player.gold >= self.tower.upg_price and self.tower.level < 2:
            self.player.gold -= self.tower.upg_price
            self.tower.upgrade()

    def upgrade_castle(self):
        if self.level == 0:
            cost = int(self.config.get('Game', 'castle_1'))
            if self.player.gold >= cost:
                self.player.gold -= cost
                self.player.health += int(self.config.get('Game',
                                                          'lvl_up_healing_1'))
                self.level += 1
            return
        if self.level == 1:
            cost = int(self.config.get('Game', 'castle_2'))
            if self.player.gold >= cost:
                self.player.gold -= cost
                self.player.health += int(self.config.get('Game',
                                                          'lvl_up_healing_2'))
                self.level += 1


class Player:

    def __init__(self):
        self.config_path = Game.conf()
        self.gold = int(config.get(self.config_path,
                                   'Player', 'gold'))
        self.towers = []
        self.health = int(config.get(self.config_path,
                                     'Player', 'health'))
        self.mana = 100

    def get_coins(self, treasure):
        self.gold += treasure

    def build_tower(self, tower, roads):
        if self.gold >= tower.price:
            for tow in self.towers:
                if (tow.location - tower.location).length < 50:
                    return
            for path in roads:
                for i in range(len(path) - 1):
                    if (path[i] - tower.location).length + \
                            (path[i + 1] - tower.location).length - \
                            (path[i + 1] - path[i]).length < 10:
                        return
            if (roads[0][len(roads[0]) - 1] - tower.location).length < 170:
                return
            self.towers.append(tower)
            self.gold -= tower.price

    def is_dead(self):
        return self.health <= 0


class Spell:

    def __init__(self, class_, game):
        self.damage = int(game.config.get(class_, 'damage'))
        self.class_ = class_
        self.image = class_

        self.full_animation = int(game.config.get(class_, 'animation'))
        self.animation = 5
        self.is_executed = False

    def invoke(self, monsters, location):
        if self.class_ == 'Thunderstorm':
            self.thunderstorm(monsters)
            return

    def thunderstorm(self, monsters):
        for monster in monsters:
            monster.get_damage(self)

    def get_image(self):
        if self.animation == self.full_animation:
            self.is_executed = True
        self.animation += 1
        return 0


class Mage:

    def __init__(self, location):
        self.location = Vector(location.X, location.Y)
        self.damage = int(config.get(Game.conf(),
                                     'Magic', 'damage_1'))
        self.level = 0
        self.price = int(config.get(Game.conf(),
                                    'Magic', 'price'))
        self.range = int(config.get(Game.conf(),
                                    'Magic', 'range_1'))
        self.upg_price = int(config.get(Game.conf(),
                                        'Magic', 'lvl_up'))
        self.attack_speed = int(config.get(Game.conf(),
                                           'Magic', 'attack_speed_1'))
        self.iter = 1
        self.pounce = 3
        self.image = 'mage'

    def fire(self, enemies):
        for enemy in enemies:
            if (enemy.location - self.location).length < self.range:
                self.iter -= 1
                if self.iter <= 0:
                    self.iter = self.attack_speed
                    return Magic(self.location, self.damage,
                                 enemy, enemies, self.pounce)
                break

    def upgrade(self):
        if self.level == 0:
            self.damage = int(config.get(Game.conf(),
                                         'Magic', 'damage_2'))
            self.range = int(config.get(Game.conf(),
                                        'Magic', 'range_2'))
            self.attack_speed = int(config.get(Game.conf(),
                                               'Magic', 'attack_speed_2'))
            self.pounce += 1
            self.level += 1
            self.iter = 1
            return
        if self.level == 1:
            self.damage = int(config.get(Game.conf(),
                                         'Magic', 'damage_3'))
            self.range = int(config.get(Game.conf(),
                                        'Magic', 'range_3'))
            self.pounce += 1
            self.attack_speed = int(config.get(Game.conf(),
                                               'Magic', 'attack_speed_3'))
            self.level += 1
            self.iter = 1


class Magic:

    def __init__(self, location, damage, target, enemies, pounce):
        self.location = Vector(location.X, location.Y)
        self.damage = damage
        self.target = target
        self.enemies = enemies
        self.pounce = pounce
        self.speed = int(config.get(Game.conf(), 'Magic', 'speed'))
        self.direction = math.pi / 2
        self.hit = False
        self.pounce_range = int(config.get(Game.conf(),
                                           'Magic', 'pounce_range'))
        self.visited = []
        self.image = 'magic'

    def move(self):
        vector = self.target.location - self.location
        if self.target.is_dead():
            self.hit = True
        if vector.length < self.target.hitbox:
            if self.target not in self.visited:
                self.target.get_damage(self)
                self.visited.append(self.target)
                self.pounce -= 1
            else:
                self.hit = True
            if self.pounce == 0:
                self.hit = True
            for creature in self.enemies:
                if creature in self.visited:
                    continue
                vector = creature.location - self.location
                if vector.length < self.pounce_range:
                    self.target = creature
                    break
        self.direction = vector.angle
        delta = Vector(math.cos(self.direction) * self.speed,
                       self.speed * math.sin(self.direction))
        self.location = self.location + delta


class PoisonTower:

    def __init__(self, location):
        self.location = Vector(location.X, location.Y)
        self.damage = int(config.get(Game.conf(), 'Poison', 'damage_1'))
        self.level = 0
        self.price = int(config.get(Game.conf(), 'Poison', 'price'))
        self.range = int(config.get(Game.conf(), 'Poison', 'range_1'))
        self.attack_speed = int(config.get(Game.conf(), 'Poison',
                                           'attack_speed_1'))
        self.slow = float(config.get(Game.conf(), 'Poison', 'slow_1'))
        self.iter = 1
        self.upg_price = int(config.get(Game.conf(), 'Poison', 'lvl_up'))
        self.image = 'poisontw'

    def fire(self, enemies):
        for enemy in enemies:
            if (enemy.location - self.location).length < self.range:
                self.iter -= 1
                if self.iter == 0:
                    self.iter = self.attack_speed
                    return Poison(self.damage,
                                  self.location, enemy, self.slow)
                break

    def upgrade(self):
        if self.level == 0:
            self.damage = int(config.get(Game.conf(), 'Poison', 'damage_2'))
            self.range = int(config.get(Game.conf(), 'Poison', 'range_2'))
            self.attack_speed = int(config.get(Game.conf(), 'Poison',
                                               'attack_speed_2'))
            self.slow = float(config.get(Game.conf(), 'Poison', 'slow_2'))
            self.level += 1
            return
        if self.level == 1:
            self.damage = int(config.get(Game.conf(), 'Poison', 'damage_3'))
            self.range = int(config.get(Game.conf(), 'Poison', 'range_3'))
            self.slow = float(config.get(Game.conf(), 'Poison', 'slow_3'))
            self.attack_speed = int(config.get(Game.conf(), 'Poison',
                                               'attack_speed_3'))
            self.level += 1


class Poison:

    def __init__(self, damage, location, enemy, slow):
        self.damage = damage
        self.location = Vector(location.X, location.Y)
        self.target = enemy
        self.slow = slow
        self.speed = int(config.get(Game.conf(), 'Poison', 'speed'))
        self.hit = False
        self.direction = math.pi / 2
        self.image = 'poison'

    def move(self):
        vector = self.target.location - self.location
        if self.target.is_dead():
            self.hit = True
        if vector.length < self.target.hitbox:
            self.target.get_damage(self)
            self.target.slow_down(self.slow)
            self.hit = True
        self.direction = vector.angle
        delta = Vector(math.cos(self.direction) * self.speed,
                       self.speed * math.sin(self.direction))
        self.location = self.location + delta


class Arrow:

    def __init__(self, start, damage, enemy):
        self.location = Vector(start.X, start.Y)
        self.damage = damage
        self.target = enemy
        self.direction = math.pi / 2
        self.hit = False
        self.speed = int(config.get(Game.conf(), 'Archers', 'speed'))
        self.image = 'arrow'

    def move(self):
        vector = self.target.location - self.location
        if vector.length < self.target.hitbox:
            self.target.get_damage(self)
            self.hit = True
        self.direction = vector.angle
        self.location += Vector(math.cos(self.direction) * self.speed,
                                math.sin(self.direction) * self.speed)


class Archers:

    def __init__(self, location):
        self.location = Vector(location.X, location.Y)
        self.damage = int(config.get(Game.conf(), 'Archers', 'damage_1'))
        self.level = 0
        self.price = int(config.get(Game.conf(), 'Archers', 'price'))
        self.range = int(config.get(Game.conf(), 'Archers', 'range_1'))
        self.upg_price = int(config.get(Game.conf(), 'Archers', 'lvl_up'))
        self.attack_speed = int(config.get(Game.conf(), 'Archers',
                                           'attack_speed_1'))
        self.iter = 1
        self.image = 'archers'

    def fire(self, enemies):
        for enemy in enemies:
            if (enemy.location - self.location).length <= self.range:
                self.iter -= 1
                if self.iter == 0:
                    self.iter = self.attack_speed
                    return Arrow(self.location, self.damage, enemy)
                break

    def upgrade(self):
        if self.level == 0:
            self.damage = int(config.get(Game.conf(), 'Archers', 'damage_2'))
            self.range = int(config.get(Game.conf(), 'Archers', 'range_2'))
            self.attack_speed = int(config.get(Game.conf(), 'Archers',
                                               'attack_speed_2'))
            self.level += 1
            self.iter = 1
            return
        if self.level == 1:
            self.damage = int(config.get(Game.conf(), 'Archers', 'damage_3'))
            self.range = int(config.get(Game.conf(), 'Archers', 'range_3'))
            self.attack_speed = int(config.get(Game.conf(), 'Archers',
                                               'attack_speed_3'))
            self.level += 1
            self.iter = 1


class Monster:

    def __init__(self, path, class_):
        self.location = Vector(path[0].X, path[0].Y)
        self.full_health = int(config.get(Game.conf(), class_, 'health'))
        self.health = self.full_health
        self.animation = 5
        self.full_animation = int(config.get(Game.conf(), class_, 'animation'))
        self.damage = int(config.get(Game.conf(), class_, 'damage'))
        self.next = 1
        self.speed = int(config.get(Game.conf(), class_, 'speed'))
        self.price = int(config.get(Game.conf(), class_, 'price'))
        self.points = path
        self.is_completed = False
        self.speed_percent = 1
        self.image = class_
        self.dir = math.pi / 2
        self.range = int(config.get(Game.conf(), class_, 'range_1'))
        self.range_2 = int(config.get(Game.conf(), class_, 'range_2'))
        self.hitbox = int(config.get(Game.conf(), class_, 'hitbox'))

    def move(self, player):
        vector = self.points[self.next] - self.location
        if self.next == len(self.points) - 1:
            self.range = self.range_2
        if vector.length < self.range:
            self.next += 1
            if self.next == len(self.points):
                self.is_completed = True
                player.health -= self.damage
                return
        self.dir = vector.angle
        delta = Vector(math.cos(self.dir) * self.speed * self.speed_percent,
                       math.sin(self.dir) * self.speed * self.speed_percent)
        self.location += delta

    def is_dead(self):
        return self.health <= 0

    def get_image(self):
        if self.animation == self.full_animation:
            self.animation = 5
        self.animation += 1
        return self.animation // 5 - 1

    def get_damage(self, source):
        self.health -= source.damage

    def heath_percents(self):
        return self.health / self.full_health

    def slow_down(self, value):
        self.speed_percent = 1 - value


class Boss:

    def __init__(self,  path, class_):
        self.location = Vector(path[0].X, path[0].Y)
        self.full_heath = int(config.get(Game.conf(), class_, 'health'))
        self.health = self.full_heath
        self.animation = 5
        self.class_ = class_
        self.damage = int(config.get(Game.conf(), class_, 'damage'))
        self.next = 1
        self.speed = int(config.get(Game.conf(), class_, 'speed'))
        self.range = int(config.get(Game.conf(), class_, 'range_1'))
        self.points = path
        self.is_completed = False
        self.finish = False
        self.range_2 = int(config.get(Game.conf(), class_, 'range_2'))
        self.speed_percent = 1
        self.immunity = config.get(Game.conf(), class_, 'immunity')
        self.image = class_
        self.dir = math.pi / 2
        self.hitbox = int(config.get(Game.conf(), class_, 'hitbox'))
        self.attack_images = config.get(Game.conf(), class_, 'attack')
        self.price = int(config.get(Game.conf(), class_, 'price'))

    def move(self, player):
        if not self.finish:
            vector = self.points[self.next] - self.location
            if self.next == len(self.points) - 1:
                self.range = self.range_2
            if vector.length < self.range:
                self.next += 1
                if self.next == len(self.points):
                    self.finish = True
                    self.image = self.attack_images
                    self.animation = 5
                    return
            self.dir = vector.angle
            df = Vector(math.cos(self.dir) * self.speed * self.speed_percent,
                        math.sin(self.dir) * self.speed * self.speed_percent)
            self.location += df
        else:
            if self.animation == 36:
                player.health -= self.damage

    def is_dead(self):
        return self.health <= 0

    def get_image(self):
        if self.animation == 36:
            self.animation = 5
        self.animation += 1
        return self.animation // 5 - 1

    def get_damage(self, source):
        if str(source.__class__) != self.immunity:
            self.health -= source.damage

    def heath_percents(self):
        return self.health / self.full_heath

    def slow_down(self, value):
        if self.class_ == 'Dragon':
            return
        self.speed_percent = 1 - value
