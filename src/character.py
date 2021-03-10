import logging
import random

from src.spell_handler import SpellHandler


class Character:
    def __init__(self):
        self.race = 'default'
        self.player_class = 'default'
        self.spell_handler = SpellHandler(self)
        self.usable_spells = []
        self.items = {}
        self.logger = logging.getLogger("simulation")

        self.base_attributes = {"base_health": 0,
                                "base_mana": 0,
                                "base_strength": 0,
                                "base_agility": 0,
                                "base_stamina": 0,
                                "base_intellect": 0,
                                "base_spirit": 0}

        self.agility = 0
        self.strength = 0
        self.intellect = 0
        self.spirit = 0
        self.stamina = 0
        self.health = 0
        self.mana = 0
        self.current_mana = 0
        self.mp5 = 0
        self.five_second_casting_counter = 0

        self.spell_crit_rating = 0
        self.spell_hit_rating = 0
        self.spell_haste_rating = 0

        self.spell_power = 0
        self.fire_power = 0
        self.arcane_power = 0
        self.frost_power = 0
        self.nature_power = 0
        self.shadow_power = 0
        self.holy_power = 0
        self.gcd_end_time = 0

    @property
    def total_health(self):
        return self.base_attributes["base_health"] + self.health + self.total_stamina * 10

    @property
    def total_mana(self):
        return self.base_attributes["base_mana"] + self.mana + self.total_intellect * 15

    @property
    def current_mana(self):
        return self.__current_mana

    @current_mana.setter
    def current_mana(self, value):
        self.__current_mana = value
        if self.__current_mana > self.total_mana:
            self.__current_mana = self.total_mana

    @property
    def is_casting(self):
        return False if self.five_second_casting_counter == 0 else True

    @property
    def total_agility(self):
        return self.agility + self.base_attributes["base_agility"]

    @property
    def total_strength(self):
        return self.strength + self.base_attributes["base_strength"]

    @property
    def total_intellect(self):
        return self.intellect + self.base_attributes["base_intellect"]

    @property
    def total_stamina(self):
        return self.stamina + self.base_attributes["base_stamina"]

    @property
    def total_spirit(self):
        return self.spirit + self.base_attributes["base_spirit"]

    @property
    def total_spell_power(self):
        return self.spell_power + self.spell_power_from_auras()

    @property
    def total_holy_power(self):
        return self.total_spell_power + self.holy_power + self.holy_power_from_auras()

    @property
    def total_fire_power(self):
        return self.total_spell_power + self.fire_power + self.fire_power_from_auras()

    @property
    def total_nature_power(self):
        return self.total_spell_power + self.nature_power + self.nature_power_from_auras()

    @property
    def total_frost_power(self):
        return self.total_spell_power + self.frost_power + self.frost_power_from_auras()

    @property
    def total_shadow_power(self):
        return self.total_spell_power + self.shadow_power + self.shadow_power_from_auras()

    @property
    def total_arcane_power(self):
        return self.total_spell_power + self.arcane_power + self.arcane_power_from_auras()

    @property
    def total_spell_hit_rating(self):
        return self.spell_hit_rating + self.spell_hit_rating_from_auras()

    @property
    def total_spell_crit_rating(self):
        return self.spell_crit_rating + self.spell_crit_rating_from_auras()

    @property
    def spell_hit_chance(self):
        return self.total_spell_hit_rating / 12.6

    @property
    def spell_crit_chance(self):
        spell_crit_gain = {
            "Warlock": 80.92,
            "Druid": 80,
            "Shaman": 80,
            "Mage": 80,
            "Priest": 80,
            "Paladin": 80.05
        }
        return self.total_spell_crit_rating / 22.1 + self.total_intellect / spell_crit_gain.get(self.player_class)

    @property
    def spell_haste_pct(self):
        return self.spell_haste_rating / 15.8

    @property
    def mp5_from_spirit(self):
        mp5_spirit_gain = {
            "Druid": self.spirit / 4.5 + 15,
            "Hunter": self.spirit / 5 + 15,
            "Paladin": self.spirit / 5 + 15,
            "Warlock": self.spirit / 5 + 15,
            "Mage": self.spirit / 4 + 12.5,
            "Priest": self.spirit / 4 + 12.5,
            "Shaman": self.spirit / 5 + 17
        }
        return mp5_spirit_gain.get(self.player_class)

    def modify_stat(self, stat_type, value):
        if stat_type == 0:
            self.mana += value
        elif stat_type == 1:
            self.health += value
        elif stat_type == 3:
            self.agility += value
        elif stat_type == 4:
            self.strength += value
        elif stat_type == 5:
            self.intellect += value
        elif stat_type == 6:
            self.spirit += value
        elif stat_type == 7:
            self.stamina += value
        elif stat_type == 18:
            self.spell_hit_rating += value
        elif stat_type == 21:
            self.spell_crit_rating += value
        elif stat_type == 30:
            self.spell_haste_rating += value
        else:
            raise NotImplementedError("Stat modification not implemented for stat_type: " + str(stat_type))

    def holy_power_from_auras(self):
        holy_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 2:
                holy_power += aura.value * aura.curr_stacks
        return holy_power

    def fire_power_from_auras(self):
        fire_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 4:
                fire_power += aura.value * aura.curr_stacks
        return fire_power

    def nature_power_from_auras(self):
        nature_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 8:
                nature_power += aura.value * aura.curr_stacks
        return nature_power

    def frost_power_from_auras(self):
        frost_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 16:
                frost_power += aura.value * aura.curr_stacks
        return frost_power

    def shadow_power_from_auras(self):
        shadow_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 32:
                shadow_power += aura.value * aura.curr_stacks
        return shadow_power

    def arcane_power_from_auras(self):
        arcane_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 64:
                arcane_power += aura.value * aura.curr_stacks
        return arcane_power

    def spell_power_from_auras(self):
        spell_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value == 126:
                spell_power += aura.value * aura.curr_stacks
        return spell_power

    def spell_hit_rating_from_auras(self):
        hit_rating = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 189 and aura.misc_value == 128:
                hit_rating += aura.value * aura.curr_stacks
        return hit_rating

    def spell_crit_rating_from_auras(self):
        crit_rating = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 189 and aura.misc_value == 1024:
                crit_rating += aura.value * aura.curr_stacks
        return crit_rating

    def spell_hit_chance_spell(self, spell_id):
        hit_chance_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 107 and aura.misc_value == 16:
                hit_chance_mod += aura.value * aura.curr_stacks
        return max(min(self.spell_hit_chance + hit_chance_mod, 16), 0)

    def spell_crit_chance_spell(self, spell_id):
        crit_chance_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 107 and aura.misc_value == 7:
                crit_chance_mod += aura.value * aura.curr_stacks
        return self.spell_crit_chance + crit_chance_mod

    def spell_crit_dmg_multiplier(self, spell_id):
        crit_damage_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 108 and aura.misc_value == 15:
                crit_damage_mod += aura.value * aura.curr_stacks
        return 1.5 + crit_damage_mod / 100

    def spell_dmg_multiplier(self, spell_id):
        spell_damage_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 108 and aura.misc_value == 22:
                spell_damage_mod += aura.value * aura.curr_stacks

        return 1 + spell_damage_mod / 100

    def spell_cast_time(self, spell_id):
        cast_time_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 107 and aura.misc_value == 10:
                cast_time_mod += aura.value * aura.curr_stacks
        cast_time = self.cast_time_with_haste(self.spell_handler.spell_cast_time(spell_id) + cast_time_mod)
        if cast_time >= 0:
            return cast_time
        return 0

    def spell_resource_cost(self, spell_id, proc_auras):
        resource_cost = self.spell_handler.spell_mana_cost(spell_id)

        for aura in self.get_mod_auras(spell_id):
            if (aura.aura_id == 108 and aura.misc_value == 14) or (aura.aura_id == 72 and aura.misc_value == 20):
                resource_cost += resource_cost * (aura.value * aura.curr_stacks / 100)
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return max(resource_cost, 0)

    def get_spell_gcd(self, spell_id):
        gcd = self.spell_handler.get_spell_gcd(spell_id)
        return max(self.cast_time_with_haste(gcd), 1000) if gcd != 0 else 0

    def can_cast_spell(self, spell_id):
        if self.current_mana >= self.spell_resource_cost(spell_id, False):
            return True
        return False

    def cast_time_with_haste(self, base_cast_time):
        return round(base_cast_time / (1 + (self.spell_haste_pct / 100)))

    def spell_power_coefficient(self, spell_id):
        coefficient_mod = 0
        for aura in self.get_mod_auras(spell_id):
            if aura.aura_id == 107 and aura.misc_value == 24:
                coefficient_mod += aura.value * aura.curr_stacks
        return self.spell_handler.spell_power_coefficient(spell_id) + coefficient_mod / 100

    def spell_spell_power(self, spell_id):
        spell_school = self.spell_handler.spell_school(spell_id)
        if spell_school == 0:
            # physical spell
            return 0
        elif spell_school == 2:
            return self.total_holy_power
        elif spell_school == 4:
            return self.total_fire_power
        elif spell_school == 8:
            return self.total_nature_power
        elif spell_school == 16:
            return self.total_frost_power
        elif spell_school == 32:
            return self.total_shadow_power
        elif spell_school == 64:
            return self.total_arcane_power
        else:
            raise ValueError("Spell school " + spell_school + " not found")

    def cast_mana_spell(self, spell_id):
        self.current_mana -= self.spell_resource_cost(spell_id, True)

    def mp5_while_casting(self):
        # TODO check for Talents
        return self.mp5

    def mp5_not_casting(self):
        return self.mp5_from_spirit + self.mp5

    def get_mod_auras(self, spell_id):
        mod_auras = []
        for aura in self.spell_handler.active_auras:
            if self.aura_applies_to_spell(aura, spell_id):
                mod_auras.append(aura)
        return mod_auras

    def aura_applies_to_spell(self, aura, spell_id):
        if aura.affected_spell_family_mask & self.spell_handler.spell_family_mask(spell_id) != 0 or \
                aura.affected_spell_school == self.spell_handler.spell_school(spell_id) or \
                aura.affected_spell_family_mask == 0:
            return True
        else:
            return False

    def process_on_spell_hit(self, spell_id):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.proc[1] > random.randint(0, 100):
                    self.handle_aura_proc(aura)

    def process_on_spell_crit(self, spell_id):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.spell_id == 11129:
                    self.spell_handler.proc_aura_charge(aura)
                if aura.proc[1] > random.randint(0, 100):
                    self.handle_aura_proc(aura)

    def handle_aura_proc(self, aura):
        # proc trigger spell
        if aura.aura_id == 42:
            self.spell_handler.apply_spell_effect(aura.trigger_spell)

        # trigger combustion aura
        if aura.spell_id == 11129:
            self.spell_handler.apply_spell_effect(28682)

    def get_procable_auras(self, proc_flag):
        procced_auras = []
        for aura in self.spell_handler.active_auras:
            if aura.proc[0] & proc_flag:
                procced_auras.append(aura)
        return procced_auras
