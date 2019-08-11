from Gameplay import *
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.start = self.game.road[0][0]
        self.path = self.game.road

    def test_enemy_move(self):
        self.game.monsters.append(Monster(self.path[0], 'Tree'))
        for i in range(0, 3):
            self.game.enemy_move()
        monster = self.game.monsters[0]
        angle = (self.path[0][1] - self.start).angle
        expected_loc = Vector(self.start.X + monster.speed *
                              monster.speed_percent * 3 * math.cos(angle),
                              self.start.Y + monster.speed *
                              monster.speed_percent * 3 * math.sin(angle))
        self.assertEqual(monster.location.X, expected_loc.X)
        self.assertEqual(monster.location.Y, expected_loc.Y)

    def test_upgrade_tower(self):
        base_gold = self.game.player.gold
        tower = Archers(Vector(500, 700))
        self.game.player.build_tower(tower, self.game.road)
        self.game.tower = tower
        self.game.upgrade_tower()
        self.assertEqual(self.game.player.gold,
                         base_gold - tower.upg_price - tower.price)
        self.assertEqual(self.game.tower.level, 1)
        self.assertIn(self.game.tower, self.game.player.towers)

    def test_tower_shooting(self):
        monster = Monster(self.path[0], 'Tree')
        tower = Archers(Vector(self.start.X + 100, self.start.Y + 100))
        self.game.player.build_tower(tower, self.path)
        self.game.fight()
        self.assertEqual(self.game.bullets, [])
        self.game.monsters.append(monster)
        self.game.fight()
        self.assertNotEqual(self.game.bullets, [])

    def test_enemy_die(self):
        monster = Monster(self.path[0], 'Tree')
        self.game.monsters.append(monster)
        base_gold = self.game.player.gold
        location = monster.location + Vector(3, 4)
        bullet = Arrow(location, monster.health + 5, monster)
        self.game.bullets.append(bullet)
        self.game.enemy_move()
        self.assertEqual(self.game.bullets, [])
        self.assertEqual(self.game.bullets, [])
        self.assertEqual(self.game.player.gold, base_gold + monster.price)
