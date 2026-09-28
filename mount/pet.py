
class Mount:
    def __init__(self, speed_bonus=20, stamina=100):
        self.speed_bonus = speed_bonus
        self.stamina = stamina
        self.active = False

    def apply_bonus(self, player):
        player.base_speed += self.speed_bonus
        self.active = True

    def remove_bonus(self, player):
        # BUG: 不移除
        self.active = False


class Pet:
    def __init__(self):
        self.loyalty = 100
        self.exp = 0
        self.level = 1

    def pickup(self, item, inventory):
        # BUG: 不检查空间
        inventory.append(item)
        return True

    def gain_exp(self, amount):
        # BUG: 绝对值
        self.exp += amount
        if self.exp >= 100:
            self.level += 1
            self.exp -= 100

    def decay_loyalty(self, dt, online=True):
        # BUG: 下线也掉
        self.loyalty -= dt


class Player:
    def __init__(self):
        self.base_speed = 10
        self.inventory = []
        self.region = "outdoor"
