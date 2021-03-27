from src.sim.handlers.spell_handler import SpellHandler
import src.db.db_connector as DB


class Character:
    def __init__(self):
        self.race = 'default'
        self.player_class = 'default'
        self.spell_handler = SpellHandler(self)
        self.damage_spells = []
        self.boost_spells = []
        self.defensive_spells = []
        self.mana_spells = []
        self.active_consumables = {}
        self.gear = {}

        self.agility = 0
        self.strength = 0
        self.intellect = 0
        self.spirit = 0
        self.stamina = 0
        self.health = 0
        self.current_health = 0
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
        return self.health + self.total_stamina * 10

    @property
    def current_health(self):
        return self.__current_health

    @current_health.setter
    def current_health(self, value):
        self.__current_health = value
        if self.__current_health > self.total_health:
            self.__current_health = self.total_health

    @property
    def total_mana(self):
        return self.mana + self.total_intellect * 15

    @property
    def current_mana(self):
        return self.__current_mana

    @current_mana.setter
    def current_mana(self, value):
        self.__current_mana = round(value)
        if self.__current_mana > self.total_mana:
            self.__current_mana = self.total_mana

    @property
    def is_casting(self):
        return False if self.five_second_casting_counter == 0 else True

    @property
    def total_agility(self):
        return round((self.agility + self.get_stat_mod(1)) * self.get_pct_stat_mod(1))

    @property
    def total_strength(self):
        return round((self.strength + self.get_stat_mod(0)) * self.get_pct_stat_mod(0))

    @property
    def total_intellect(self):
        return round((self.intellect + self.get_stat_mod(3)) * self.get_pct_stat_mod(3))

    @property
    def total_stamina(self):
        return round((self.stamina + self.get_stat_mod(2)) * self.get_pct_stat_mod(2))

    @property
    def total_spirit(self):
        return round((self.spirit + self.get_stat_mod(4)) * self.get_pct_stat_mod(4))

    @property
    def total_holy_power(self):
        return self.spell_power + self.holy_power + self.school_power_from_auras(2)

    @property
    def total_fire_power(self):
        return self.spell_power + self.fire_power + self.school_power_from_auras(4)

    @property
    def total_nature_power(self):
        return self.spell_power + self.nature_power + self.school_power_from_auras(8)

    @property
    def total_frost_power(self):
        return self.spell_power + self.frost_power + self.school_power_from_auras(16)

    @property
    def total_shadow_power(self):
        return self.spell_power + self.shadow_power + self.school_power_from_auras(32)

    @property
    def total_arcane_power(self):
        return self.spell_power + self.arcane_power + self.school_power_from_auras(64)

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
        return self.total_spell_crit_rating / 22.1 \
               + self.total_intellect / spell_crit_gain.get(self.player_class) \
               + 0.91

    @property
    def spell_haste_pct(self):
        return self.spell_haste_rating / 15.75

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

    def get_pct_stat_mod(self, stat_index, proc_auras=True):
        stat_pct_mod = 100
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 137 and aura.misc_value == stat_index:
                stat_pct_mod += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return stat_pct_mod / 100

    def get_stat_mod(self, stat_index, proc_auras=True):
        stat_mod = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 29 and aura.misc_value == stat_index:
                stat_mod += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return stat_mod

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

    def school_power_from_auras(self, spell_school, proc_auras=True):
        school_power = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 13 and aura.misc_value & spell_school:
                school_power += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
            elif aura.aura_id == 174 and aura.misc_value & spell_school:
                school_power += self.total_intellect * (aura.value * aura.curr_stacks / 100)
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return school_power

    def spell_hit_rating_from_auras(self, proc_auras=True):
        hit_rating = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 189 and aura.misc_value == 128:
                hit_rating += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return hit_rating

    def spell_crit_rating_from_auras(self, proc_auras=True):
        crit_rating = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 189 and aura.misc_value == 1024:
                crit_rating += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return crit_rating

    def spell_hit_chance_spell(self, spell_id=0, proc_auras=True):
        hit_chance_mod = 0
        if spell_id != 0:
            # for aura in self.spell_handler.get_character_mod_auras(spell_id):
            for aura in self.spell_handler.active_auras:
                if self.spell_handler.aura_applies_to_spell(aura, spell_id) and \
                        (aura.aura_id == 107 and aura.misc_value == 16 and aura.spell_id not in [29438, 29439, 29440] or
                         aura.aura_id == 107 and aura.misc_value == 16 and
                         aura.affected_spell_family_mask & DB.get_spell_family(spell_id)):
                    hit_chance_mod += aura.value * aura.curr_stacks

                    if proc_auras:
                        self.spell_handler.proc_aura_charge(aura)
        return max(min(self.spell_hit_chance + hit_chance_mod, 16), 0)

    def spell_crit_chance_spell(self, spell_id=0, proc_auras=True):
        crit_chance_mod = 0
        if spell_id != 0:

            for aura in self.spell_handler.active_auras:
                if self.spell_handler.aura_applies_to_spell(aura, spell_id) and \
                        (aura.aura_id == 107 and aura.misc_value == 7 and
                         (aura.spell_id not in [31682, 31683, 31684, 31685, 31686] or
                          aura.affected_spell_school & DB.get_spell_school(spell_id) or
                          aura.affected_spell_family_mask & DB.get_spell_family(spell_id)) and
                         (aura.spell_id not in [11108, 12349, 12350] or DB.get_spell_family(spell_id) & 4) or
                         aura.aura_id == 71 and aura.misc_value == 126 or
                         aura.aura_id == 71 and aura.misc_value == DB.get_spell_school(spell_id) or
                         aura.aura_id == 57):

                    # Apply spell crit modifier from mage incineration talent only if spell scorch or fire blast
                    if aura.spell_id not in (18459, 18460) or \
                            self.spell_handler.spell_family_mask(spell_id) & 2 or \
                            self.spell_handler.spell_family_mask(spell_id) & 16:
                        crit_chance_mod += aura.value * aura.curr_stacks

                        if proc_auras:
                            self.spell_handler.proc_aura_charge(aura)
                elif aura.spell_id in [11170, 12982, 12983, 12984, 12985] and \
                        any(aura.spell_id == 12494 for aura in self.spell_handler.enemy.active_auras):
                    shatter_crit_chance = {
                        11170: 10,
                        12982: 20,
                        12983: 30,
                        12984: 40,
                        12985: 50
                    }
                    crit_chance_mod += shatter_crit_chance.get(aura.spell_id) * aura.curr_stacks

            for aura in self.spell_handler.enemy.active_auras:
                if DB.get_spell_school(spell_id) == 16 and aura.spell_id == 12579:
                    crit_chance_mod += aura.value * aura.curr_stacks

        return round(self.spell_crit_chance + crit_chance_mod, 3)

    def spell_crit_dmg_multiplier(self, spell_id, proc_auras=True):
        crit_damage_mod = 0

        for aura in self.spell_handler.active_auras:
            if self.spell_handler.aura_applies_to_spell(aura, spell_id) and \
                    aura.aura_id == 108 and aura.misc_value == 15 or \
                    aura.aura_id == 163 and aura.misc_value == 895:
                crit_damage_mod += aura.value * aura.curr_stacks

                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return 1.5 * (1 + crit_damage_mod / 100)

    def spell_dmg_multiplier(self, spell_id, proc_auras=True):
        spell_damage_multiplier = 1

        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 108 and aura.misc_value == 22 or \
                    aura.aura_id == 108 and aura.misc_value == 0 and \
                    aura.affected_spell_school & DB.get_spell_school(spell_id) or \
                    aura.aura_id == 79 and aura.misc_value & DB.get_spell_school(spell_id) and \
                    aura.affected_item_class <= 0 or \
                    aura.spell_id in [11190, 12489, 12490] and DB.get_spell_family(spell_id) & 512 or \
                    aura.spell_id in [31679, 31680] and self.spell_handler.enemy.in_execute_range or \
                    aura.aura_id == 79 and aura.spell_id in (15058, 15059, 15060, 31638, 31639, 31640):
                spell_damage_multiplier *= 1 + (aura.value * aura.curr_stacks / 100)

                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)

        return spell_damage_multiplier

    def wand_dmg_multiplier(self, proc_auras=True):
        wand_damage_multiplier = 1

        for aura in self.spell_handler.active_auras:
            if aura.affected_item_class == 2 and aura.affected_item_subclass_mask & (1 << 19) and \
                    (aura.aura_id == 79 and aura.misc_value == 126):
                wand_damage_multiplier *= 1 + (aura.value * aura.curr_stacks / 100)
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)

        return wand_damage_multiplier

    def spell_cast_time(self, spell_id, proc_auras=True):
        cast_time_mod_pct = 1
        cast_time_mod_flat = 0
        # for aura in self.spell_handler.get_character_mod_auras(spell_id):
        for aura in self.spell_handler.active_auras:
            if self.spell_handler.aura_applies_to_spell(aura, spell_id):
                if aura.aura_id == 107 and aura.misc_value == 10 and\
                        (aura.spell_id not in [11069, 12338, 12339, 12340, 12341] or DB.get_spell_family(spell_id) & 1):
                    cast_time_mod_flat += aura.value * aura.curr_stacks
                    if proc_auras:
                        self.spell_handler.proc_aura_charge(aura)
                elif aura.aura_id == 65:
                    cast_time_mod_pct *= 1 - (aura.value * aura.curr_stacks / 100)
                    if proc_auras:
                        self.spell_handler.proc_aura_charge(aura)
                elif aura.aura_id == 108 and aura.misc_value == 10:
                    cast_time_mod_pct *= (aura.value * aura.curr_stacks / 100)
                    if proc_auras:
                        self.spell_handler.proc_aura_charge(aura)

        cast_time = self.cast_time_with_haste(self.spell_handler.spell_cast_time(spell_id) + cast_time_mod_flat) \
                    * cast_time_mod_pct
        if cast_time >= 0:
            return round(cast_time)
        return 0

    def spell_resource_cost(self, spell_id, proc_auras=True):
        resource_cost = self.spell_handler.spell_flat_mana_cost(spell_id) \
                        + (self.spell_handler.spell_pct_mana_cost(spell_id) / 100) * self.total_mana

        # for aura in self.spell_handler.get_character_mod_auras(spell_id):
        for aura in self.spell_handler.active_auras:
            if self.spell_handler.aura_applies_to_spell(aura, spell_id) and \
                    ((aura.aura_id == 108 and aura.misc_value == 14) and
                     (aura.spell_id not in [31579, 31582, 31583] or DB.get_spell_family(spell_id) & 2048) or
                     (aura.aura_id == 72 and (aura.misc_value & DB.get_spell_school(spell_id)))):
                resource_cost *= 1 + (aura.value * aura.curr_stacks / 100)

                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return max(round(resource_cost), 0)

    def get_spell_gcd(self, spell_id):
        gcd = self.spell_handler.get_spell_gcd(spell_id)
        return max(self.cast_time_with_haste(gcd), 1000) if gcd != 0 else 0

    def has_mana_to_cast_spell(self, spell_id):
        if self.current_mana >= self.spell_resource_cost(spell_id, False):
            return True
        return False

    def cast_time_with_haste(self, base_cast_time):
        return round(base_cast_time / (1 + (self.spell_haste_pct / 100)))

    def spell_power_coefficient(self, spell_id, proc_auras=True):
        coefficient_mod = 0
        # for aura in self.spell_handler.get_character_mod_auras(spell_id):
        for aura in self.spell_handler.active_auras:
            if self.spell_handler.aura_applies_to_spell(aura, spell_id) and \
                    (aura.aura_id == 107 and aura.misc_value == 24):
                coefficient_mod += aura.value * aura.curr_stacks
                if proc_auras:
                    self.spell_handler.proc_aura_charge(aura)
        return self.spell_handler.spell_power_coefficient(spell_id) + coefficient_mod / 100

    def spell_spell_power(self, spell_id):
        spell_school = DB.get_spell_school(spell_id)
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
        spirit_mp5_casting = 0
        for aura in self.spell_handler.active_auras:
            if aura.aura_id == 134:
                spirit_mp5_casting += aura.value * aura.curr_stacks
        return self.mp5 + self.mp5_from_spirit * (spirit_mp5_casting / 100)

    def mp5_not_casting(self):
        return self.mp5_from_spirit + self.mp5

    def has_wand_range_attack(self):
        return 18 in self.gear and \
               self.gear[18].item_data[DB.item_column_info["class"]] == 2 and \
               self.gear[18].item_data[DB.item_column_info["subclass"]] == 19

    def weapon_attack_delay_time(self, inventory_slot):
        return self.gear[inventory_slot].item_data[DB.item_column_info["delay"]]

    def get_weapon_damage(self, inventory_slot):
        return self.gear[inventory_slot].item_data[DB.item_column_info["dmg_min1"]], \
               self.gear[inventory_slot].item_data[DB.item_column_info["dmg_max1"]]
