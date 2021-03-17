class Enemy(object):
    def __init__(self):
        self.attributes = {"armor": 0,
                           "holy_resistance": 0,
                           "frost_resistance": 0,
                           "fire_resistance": 0,
                           "nature_resistance": 0,
                           "arcane_resistance": 0,
                           "shadow_resistance": 0}
        self.active_auras = []
        self.in_execute_range = False

        self.level = 0
        self.boss = 0
