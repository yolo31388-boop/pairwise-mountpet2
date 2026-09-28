class SpeedModifier:
    """速度修饰器：上马应用、下马移除，不直接改基础速度。"""

    def __init__(self, source, amount):
        self.source = source
        self.amount = amount


class Mount:
    ALLOWED_SUMMON_REGIONS = {"outdoor"}
    STAMINA_RATES = {"run": 5, "fly": 15, "swim": 8}

    def __init__(self, speed_bonus=20, stamina=100):
        self.speed_bonus = speed_bonus
        self.stamina = stamina
        self.active = False
        self._modifier = SpeedModifier("mount", speed_bonus)

    def can_summon(self, player):
        return getattr(player, "region", "outdoor") in self.ALLOWED_SUMMON_REGIONS

    def apply_bonus(self, player):
        if not hasattr(player, "modifiers"):
            player.modifiers = []
        if self._modifier not in player.modifiers:
            player.modifiers.append(self._modifier)
        player.base_speed += self._modifier.amount
        self.active = True

    def remove_bonus(self, player):
        if hasattr(player, "modifiers") and self._modifier in player.modifiers:
            player.modifiers.remove(self._modifier)
            player.base_speed -= self._modifier.amount
        self.active = False

    def consume_stamina(self, dt, mode="run"):
        rate = self.STAMINA_RATES.get(mode, self.STAMINA_RATES["run"])
        self.stamina = max(0, self.stamina - rate * dt)
        return self.stamina


class Pet:
    BASE_EXP = 100

    def __init__(self):
        self.loyalty = 100
        self.exp = 0
        self.level = 1
        self.skill_cd = 0  # 独立于主人的冷却计时器

    def exp_needed(self, level=None):
        level = self.level if level is None else level
        return self.BASE_EXP * level

    def pickup(self, item, inventory, cap=None):
        if cap is None:
            cap = getattr(item, "inventory_cap", None)
        if cap is None:
            cap = 10
        if len(inventory) >= cap:
            return False
        inventory.append(item)
        return True

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_needed():
            self.exp -= self.exp_needed()
            self.level += 1

    def decay_loyalty(self, dt, online=True, fed=False):
        if not online or fed:
            return
        self.loyalty = max(0, self.loyalty - dt)


class Player:
    def __init__(self):
        self.base_speed = 10
        self.inventory = []
        self.inventory_cap = 10
        self.region = "outdoor"
        self.modifiers = []
        self.skill_cd = 0
