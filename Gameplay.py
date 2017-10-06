from Vectors import Vector
import math
import threading
import time
import config
import os


class Game:
    def __init__(self):
        path = Game.get_config()
        config.create_config(path)
        self.config = config.get_config(path)
        self.bullets = []
        self.road = [Vector(0, 350), Vector(1000, 350)]
        self.start = self.road[0]
        self.player = Player()
        self.level = 0
        self.tower = None
        self.game_level = 0
        self.creatures = []
        self.lock = threading.Lock()
        self.spawn = threading.Thread(target=self.create)

    def start_game(self):
        self.spawn.start()

    @staticmethod
    def get_config():
        return os.getcwd() + '\Config.ini'

    def create(self):
        tree = 'Tree'
        skeleton = 'Skeleton'
        time.sleep(7)
        self.creatures.append(Monster(self.start, self.road, skeleton))
        for i in range(4):
            self.lock.acquire()
            self.creatures.append(Monster(self.start, self.road, skeleton))
            self.lock.release()
            time.sleep(1)
        self.creatures.append(Monster(self.start, self.road, tree))
        time.sleep(0.5)
        self.creatures.append(Monster(self.start, self.road, skeleton))
        time.sleep(0.5)
        self.creatures.append(Monster(self.start, self.road, tree))
        time.sleep(0.25)
        self.creatures.append(Monster(self.start, self.road, skeleton))
        for i in range(6):
            self.creatures.append(Monster(self.start, self.road, tree))
            time.sleep(0.25)
            self.creatures.append(Monster(self.start, self.road, skeleton))
            time.sleep(3)
        self.lock.acquire()
        self.creatures.append(Dragon(self.start, self.road))
        self.lock.release()
        while len(self.creatures) != 0:
            time.sleep(1)
        self.change_level([Vector(0, 200), Vector(400, 200),
                           Vector(400, 500), Vector(1000, 500)])
        time.sleep(7)
        for i in range(10):
            self.lock.acquire()
            self.creatures.append(Monster(self.start, self.road, tree))
            self.lock.release()
            time.sleep(0.25)
            self.lock.acquire()
            self.creatures.append(Monster(self.start, self.road, skeleton))
            self.lock.release()
            time.sleep(0.5)
        self.lock.acquire()
        self.creatures.append(Dragon(self.start, self.road))
        self.lock.release()
        time.sleep(5)
        for i in range(10):
            self.lock.acquire()
            self.creatures.append(Monster(self.start, self.road, tree))
            self.lock.release()
            time.sleep(0.25)
            self.lock.acquire()
            self.creatures.append(Monster(self.start, self.road, skeleton))
            self.lock.release()
        self.creatures.append(Dragon(self.start, self.road))

    def fight(self):
        for tower in self.player.towers:
            bullet = tower.fire(self.creatures)
            if bullet is not None:
                self.bullets.append(bullet)

    def enemy_move(self):
        self.lock.acquire()
        for enemy in self.creatures:
            enemy.move(self.player)
            if enemy.is_completed:
                self.creatures.remove(enemy)
        self.lock.release()
        for bullet in self.bullets:
            bullet.move()
        self.bullets = list(filter(lambda x: not x.hit, self.bullets))
        dead = list(filter(lambda x: x.is_dead(), self.creatures))
        self.lock.acquire()
        for e in dead:
            self.player.get_coins(e.price)
            self.creatures.remove(e)
        self.lock.release()
        self.bullets = list(filter(lambda x: not x.hit, self.bullets))

    def change_level(self, next_path):
        self.bullets.clear()
        self.player.towers.clear()
        self.road = next_path
        self.start = self.road[0]
        self.player.gold += int(self.config.get('Player_Settings','level_reward'))
        self.tower = None
        self.game_level += 1

    def upgrade_tower(self):
        if self.player.gold >= self.tower.upg_price and self.tower.level < 2:
            self.player.gold -= self.tower.upg_price
            self.tower.upgrade()

    def upgrade_castle(self):
        if self.level == 0:
            cost = int(self.config.get('Game','castle_1'))
            if self.player.gold >= cost:
                self.player.gold -= cost
                self.player.health += int(self.config.get('Game','lvl_up_healing_1'))
                self.level += 1
            return
        if self.level == 1:
            cost = int(self.config.get('Game','castle_2'))
            if self.player.gold >= cost:
                self.player.gold -= cost
                self.player.health += int(self.config.get('Game','lvl_up_healing_2'))
                self.level += 1


class Player:

    def __init__(self):
        self.config_path = Game.get_config()
        self.gold = int(config.get_setting(self.config_path,'Player_Settings','gold'))
        self.towers = []
        self.health = int(config.get_setting(self.config_path,'Player_Settings','health'))

    def get_coins(self, treasure):
        self.gold += treasure

    def build_tower(self, tower, path):
        if self.gold >= tower.price:
            for tow in self.towers:
                if (tow.location - tower.location).length < 50:
                    return
            for i in range(len(path) - 1):
                if (path[i] - tower.location).length + \
                        (path[i + 1] - tower.location).length - \
                        (path[i + 1] - path[i]).length < 10:
                    return
            if (path[len(path) - 1] - tower.location).length < 170:
                return
            self.towers.append(tower)
            self.gold -= tower.price

    def is_dead(self):
        return self.health <= 0



class Mage:

    def __init__(self, location):
        self.location = Vector(location.X, location.Y)
        self.damage = int(config.get_setting(Game.get_config(),'Magic', 'damage_1'))
        self.level = 0
        self.price = int(config.get_setting(Game.get_config(),'Magic', 'price'))
        self.range = int(config.get_setting(Game.get_config(),'Magic', 'range_1'))
        self.upg_price = int(config.get_setting(Game.get_config(),'Magic', 'lvl_up'))
        self.attack_speed = int(config.get_setting(Game.get_config(),'Magic', 'attack_speed_1'))
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
            self.damage = int(config.get_setting(Game.get_config(),'Magic', 'damage_2'))
            self.range = int(config.get_setting(Game.get_config(),'Magic', 'range_2'))
            self.attack_speed = int(config.get_setting(Game.get_config(),'Magic', 'attack_speed_2'))
            self.pounce += 1
            self.level += 1
            self.iter = 1
            return
        if self.level == 1:
            self.damage = int(config.get_setting(Game.get_config(),'Magic', 'damage_3'))
            self.range = int(config.get_setting(Game.get_config(),'Magic', 'range_3'))
            self.pounce += 1
            self.attack_speed = int(config.get_setting(Game.get_config(),'Magic', 'attack_speed_3'))
            self.level += 1
            self.iter = 1


class Magic:

    def __init__(self, location, damage, target, enemies, pounce):
        self.location = Vector(location.X, location.Y)
        self.damage = damage
        self.target = target
        self.enemies = enemies
        self.pounce = pounce
        self.speed = int(config.get_setting(Game.get_config(),'Magic', 'speed'))
        self.direction = math.pi / 2
        self.hit = False
        self.pounce_range = int(config.get_setting(Game.get_config(),'Magic', 'pounce_range'))
        self.visited = []
        self.image = 'magic'

    def move(self):
        vector = self.target.location - self.location
        if self.target.is_dead():
            self.hit = True
        if vector.length < self.target.hitbox:
            if self.target not in self.visited:
                self.target.get_damage(self.damage)
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
        self.damage = int(config.get_setting(Game.get_config(),'Poison', 'damage_1'))
        self.level = 0
        self.price = int(config.get_setting(Game.get_config(),'Poison', 'price'))
        self.range = int(config.get_setting(Game.get_config(),'Poison', 'range_1'))
        self.attack_speed = int(config.get_setting(Game.get_config(),'Poison', 'attack_speed_1'))
        self.slow = float(config.get_setting(Game.get_config(),'Poison', 'slow_1'))
        self.iter = 1
        self.upg_price = int(config.get_setting(Game.get_config(),'Poison', 'lvl_up'))
        self.image = 'poisontw'

    def fire(self, enemies):
        for enemy in enemies:
            if (enemy.location - self.location).length < self.range:
                self.iter -= 1
                if self.iter == 0:
                    self.iter = self.attack_speed
                    return Poison(self.damage, self.location, enemy, self.slow)
                break

    def upgrade(self):
        if self.level == 0:
            self.damage = int(config.get_setting(Game.get_config(),'Poison', 'damage_2'))
            self.range = int(config.get_setting(Game.get_config(),'Poison', 'range_2'))
            self.attack_speed = int(config.get_setting(Game.get_config(),'Poison', 'attack_speed_2'))
            self.slow = float(config.get_setting(Game.get_config(),'Poison', 'slow_2'))
            self.level += 1
            return
        if self.level == 1:
            self.damage = int(config.get_setting(Game.get_config(),'Poison', 'damage_3'))
            self.range = int(config.get_setting(Game.get_config(),'Poison', 'range_3'))
            self.slow = float(config.get_setting(Game.get_config(),'Poison', 'slow_3'))
            self.attack_speed = int(config.get_setting(Game.get_config(),'Poison', 'attack_speed_3'))
            self.level += 1


class Poison:

    def __init__(self, damage, location, enemy, slow):
        self.damage = damage
        self.location = Vector(location.X, location.Y)
        self.target = enemy
        self.slow = slow
        self.speed = int(config.get_setting(Game.get_config(),'Poison', 'speed'))
        self.hit = False
        self.direction = math.pi / 2
        self.image = 'poison'

    def move(self):
        vector = self.target.location - self.location
        if self.target.is_dead():
            self.hit = True
        if vector.length < self.target.hitbox:
            self.target.get_damage(self.damage)
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
        self.speed = int(config.get_setting(Game.get_config(),'Archers', 'speed'))
        self.image = 'arrow'

    def move(self):
        vector = self.target.location - self.location
        if vector.length < self.target.hitbox:
            self.target.get_damage(self.damage)
            self.hit = True
        self.direction = vector.angle
        self.location += Vector(math.cos(self.direction) * self.speed,
                                math.sin(self.direction) * self.speed)


class Archers:

    def __init__(self, location):
        self.location = Vector(location.X, location.Y)
        self.damage = int(config.get_setting(Game.get_config(),'Archers', 'damage_1'))
        self.level = 0
        self.price = int(config.get_setting(Game.get_config(),'Archers', 'price'))
        self.range = int(config.get_setting(Game.get_config(),'Archers', 'range_1'))
        self.upg_price = int(config.get_setting(Game.get_config(),'Archers', 'lvl_up'))
        self.attack_speed = int(config.get_setting(Game.get_config(),'Archers', 'attack_speed_1'))
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
            self.damage = int(config.get_setting(Game.get_config(),'Archers', 'damage_2'))
            self.range = int(config.get_setting(Game.get_config(),'Archers', 'range_2'))
            self.attack_speed = int(config.get_setting(Game.get_config(),'Archers', 'attack_speed_2'))
            self.level += 1
            self.iter = 1
            return
        if self.level == 1:
            self.damage = int(config.get_setting(Game.get_config(),'Archers', 'damage_3'))
            self.range = int(config.get_setting(Game.get_config(),'Archers', 'range_3'))
            self.attack_speed = int(config.get_setting(Game.get_config(),'Archers', 'attack_speed_3'))
            self.level += 1
            self.iter = 1

class Monster:

    def __init__(self, start, path,class_):
        self.location = Vector(start.X, start.Y)
        self.full_health = int(config.get_setting(Game.get_config(),class_, 'health'))
        self.health = self.full_health
        self.animation = 5
        self.full_animation = int(config.get_setting(Game.get_config(),class_, 'animation'))
        self.damage = int(config.get_setting(Game.get_config(),class_, 'damage'))
        self.next = path.index(start) + 1
        self.speed = int(config.get_setting(Game.get_config(),class_, 'speed'))
        self.price = int(config.get_setting(Game.get_config(),class_, 'price'))
        self.points = path
        self.is_completed = False
        self.speed_percent = 1
        self.image = class_
        self.range = int(config.get_setting(Game.get_config(),class_, 'range_1'))
        self.hitbox = int(config.get_setting(Game.get_config(),class_, 'hitbox'))

    def move(self, player):
        vector = self.points[self.next] - self.location
        if self.next == len(self.points) - 1:
            self.range = int(config.get_setting(Game.get_config(),self.image, 'range_2'))
        if vector.length < self.range:
            self.next += 1
            if self.next == len(self.points):
                self.is_completed = True
                player.health -= self.damage
        direction = vector.angle
        delta = Vector(math.cos(direction) * self.speed * self.speed_percent,
                       math.sin(direction) * self.speed * self.speed_percent)
        self.location += delta

    def is_dead(self):
        return self.health <= 0

    def get_image(self):
        if self.animation == self.full_animation:
            self.animation = 5
        self.animation += 1
        return self.animation // 5 - 1

    def get_damage(self, damage):
        self.health -= damage

    def heath_percents(self):
        return self.health / self.full_health

    def slow_down(self, value):
        self.speed_percent = 1 - value


class Dragon:

    def __init__(self, start, path):
        self.location = Vector(start.X, start.Y)
        self.full_heath = int(config.get_setting(Game.get_config(),'Dragon', 'health'))
        self.health = self.full_heath
        self.animation = 5
        self.damage = int(config.get_setting(Game.get_config(),'Dragon', 'damage'))
        self.next = path.index(start) + 1
        self.speed = int(config.get_setting(Game.get_config(),'Dragon', 'speed'))
        self.range = int(config.get_setting(Game.get_config(),'Dragon', 'range_1'))
        self.points = path
        self.is_completed = False
        self.finish = False
        self.speed_percent = 1
        self.image = 'dragon'
        self.hitbox = int(config.get_setting(Game.get_config(),'Dragon', 'hitbox'))
        self.price = int(config.get_setting(Game.get_config(),'Dragon', 'price'))

    def move(self, player):
        if not self.finish:
            vector = self.points[self.next] - self.location
            if self.next == len(self.points) - 1:
                self.range = int(config.get_setting(Game.get_config(),'Dragon', 'range_2'))
            if vector.length < self.range:
                self.next += 1
                if self.next == len(self.points):
                    self.finish = True
                    self.image = 'dragonAttack'
                    self.animation = 5
                    return
            dir = vector.angle
            delta = Vector(math.cos(dir) * self.speed * self.speed_percent,
                           math.sin(dir) * self.speed * self.speed_percent)
            self.location += delta
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

    def get_damage(self, damage):
        self.health -= damage

    def heath_percents(self):
        return self.health / self.full_heath

    def slow_down(self, value):
        self.speed_percent = 1 - value
