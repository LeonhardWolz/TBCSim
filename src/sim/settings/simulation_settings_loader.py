import random
import re

import copy
import src.db.sqlite_db_connector as DB

from src import enums
from src.sim.exceptions.exceptions import NotImplementedWarning
from src.sim.results.sim_cumulative_result import SimCumResult
from src.sim.sim_objects.enemy import Enemy

from src.sim.settings.sim_settings import SimSettings
from src.sim.sim_objects.character import Character
from src.sim.results.sim_results import EquippedItem


class SimulationSettingsLoader(object):
    mage_boost_spells = (11129, 12472)

    mage_mana_spells = (12051,)

    def __init__(self, settings_dict):
        self.char = []
        self.enemy = Enemy()
        self.simSettings = SimSettings()
        self.sim_results = SimCumResult()

        self.load_settings(settings_dict)
        self.sim_results.char = copy.deepcopy(self.char)

    def load_settings(self, settings_dict):
        # load sim settings
        self.load_sim_settings(settings_dict["simulation"])

        # load enemy settings
        self.load_enemy_settings(settings_dict["enemy"])

        for x, char_dict in enumerate(settings_dict["character"].values()):
            self.char.append(Character())
            # load character settings
            self.load_character_settings(x, char_dict)

            self.char[x].current_health = self.char[x].total_health
            self.char[x].current_mana = self.char[x].total_mana
            self.char[x].combat_handler.enemy = self.enemy

    def load_sim_settings(self, sim_settings):
        self.simSettings.sim_type = sim_settings["sim_type"] \
            if "sim_type" in sim_settings else "dps"

        self.simSettings.sim_duration = sim_settings["sim_duration"] * 1000 \
            if "sim_duration" in sim_settings else 300000

        self.simSettings.sim_iterations = sim_settings["sim_iterations"] \
            if "sim_iterations" in sim_settings else 1

        self.simSettings.results_file_path = sim_settings["results_file_path"] \
            if "results_file_path" in sim_settings else None

        self.simSettings.full_log_for_best = sim_settings["full_log_for_best"] \
            if "full_log_for_best" in sim_settings else False

        self.simSettings.sim_combat_rater = sim_settings["sim_combat_rater"] \
            if "sim_combat_rater" in sim_settings else None

    def load_enemy_settings(self, enemy_settings):
        self.enemy.attributes["armor"] = enemy_settings["attributes"]["armor"]
        self.enemy.attributes["holy_resistance"] = enemy_settings["attributes"]["holy_resistance"]
        self.enemy.attributes["frost_resistance"] = enemy_settings["attributes"]["frost_resistance"]
        self.enemy.attributes["fire_resistance"] = enemy_settings["attributes"]["fire_resistance"]
        self.enemy.attributes["nature_resistance"] = enemy_settings["attributes"]["nature_resistance"]
        self.enemy.attributes["arcane_resistance"] = enemy_settings["attributes"]["arcane_resistance"]
        self.enemy.attributes["shadow_resistance"] = enemy_settings["attributes"]["shadow_resistance"]

        self.enemy.level = enemy_settings["level"]
        self.enemy.boss = enemy_settings["boss"]

    def load_character_settings(self, char_index, char_settings):
        # load base stats for race and class specified in settings
        base_stats = DB.get_base_stats(enums.PlayerClass[char_settings["class"]].value,
                                       enums.Race[char_settings["race"]].value)

        self.char[char_index].modify_stat(1, base_stats[2])
        self.char[char_index].modify_stat(0, base_stats[3])
        self.char[char_index].modify_stat(4, base_stats[7])
        self.char[char_index].modify_stat(3, base_stats[8])
        self.char[char_index].modify_stat(7, base_stats[9])
        self.char[char_index].modify_stat(5, base_stats[10])
        self.char[char_index].modify_stat(6, base_stats[11])

        self.char[char_index].race = char_settings["race"]
        self.char[char_index].player_class = char_settings["class"]

        self.load_racials(char_index)
        self.load_spells(char_index, char_settings)

        self.load_consumables(char_index, char_settings)

        self.load_character_items(char_index, char_settings["gear"])
        self.load_talents(char_index, char_settings)

    def load_racials(self, char_index):
        if self.char[char_index].race == "Human":
            self.char[char_index].combat_handler.apply_spell_effect(20598)
        elif self.char[char_index].race == "Orc":
            pass
        elif self.char[char_index].race == "Dwarf":
            self.char[char_index].combat_handler.apply_spell_effect(20595)
            self.char[char_index].combat_handler.apply_spell_effect(20596)
        elif self.char[char_index].race == "Nightelf":
            self.char[char_index].combat_handler.apply_spell_effect(20583)
        elif self.char[char_index].race == "Undead":
            self.char[char_index].combat_handler.apply_spell_effect(20579)
        elif self.char[char_index].race == "Tauren":
            self.char[char_index].combat_handler.apply_spell_effect(20551)
            self.char[char_index].combat_handler.apply_spell_effect(20550)
        elif self.char[char_index].race == "Gnome":
            self.char[char_index].combat_handler.apply_spell_effect(20592)
            self.char[char_index].combat_handler.apply_spell_effect(20591)
        elif self.char[char_index].race == "Troll":
            self.char[char_index].boost_spells.append(20554)
        elif self.char[char_index].race == "Bloodelf":
            self.char[char_index].combat_handler.apply_spell_effect(822)
        elif self.char[char_index].race == "Draenei":
            self.char[char_index].combat_handler.apply_spell_effect(6562)
            self.char[char_index].combat_handler.apply_spell_effect(28878)
            self.char[char_index].combat_handler.apply_spell_effect(20579)

    def load_consumables(self, char_index, char_settings):
        for consumable_id in char_settings["passive_consumables"]:
            self.char[char_index].passive_consumables.append(consumable_id)
            item_info = DB.get_item(consumable_id)
            for i in range(1, 4):
                spell_id = item_info[DB.item_column_info["spellid_" + str(i)]]
                if spell_id != 0:
                    # bufffood triggers spell
                    triggered_spell_id = self.char[char_index].combat_handler.spell_get_triggered_spell(spell_id)
                    try:
                        if triggered_spell_id != 0:
                            self.char[char_index].combat_handler.apply_spell_effect(triggered_spell_id)
                        else:
                            self.char[char_index].combat_handler.apply_spell_effect(spell_id)
                    except NotImplementedWarning as e:
                        self.sim_results.errors.append(str(e))

        if char_settings["active_consumables"]:
            for consumable_id in char_settings["active_consumables"]:
                self.char[char_index].active_consumables[consumable_id] = 0

    def load_spells(self, char_index, char_settings):
        for spell_id in char_settings["active_spells"]:
            self.char[char_index].damage_spells.append(spell_id)

        for spell_id in char_settings["passive_spells"]:
            self.char[char_index].passive_spells.append(spell_id)
            self.char[char_index].combat_handler.apply_spell_effect(spell_id)

        if self.char[char_index].player_class == "Mage":
            for spell_id in self.mage_mana_spells:
                self.char[char_index].mana_spells.append(spell_id)

    def load_talents(self, char_index, settings):
        if "talent_calc_link" in settings and "tbc.wowhead" in settings["talent_calc_link"]:
            self.char[char_index].talents = settings["talent_calc_link"]
            talent_string = re.findall("/([0-9-]+)", settings["talent_calc_link"])
            talent_strings = talent_string[0].split("-")

            for x, group in enumerate(talent_strings):
                talent_tab_id = DB.get_talent_tab_id(enums.PlayerClass[self.char[char_index].player_class].value, x)
                for index, talent_rank in enumerate(group):
                    if talent_rank != "0":
                        talent_id = DB.get_talent_id(talent_tab_id, index, talent_rank)
                        self.load_talent(char_index, talent_id)
        else:
            self.char[char_index].talents = "None"

    def load_talent(self, char_index, talent_id):
        talent_info = DB.get_spell(talent_id)
        if talent_info[DB.spell_column_info["Attributes"]] & 0x00000040:
            self.char[char_index].combat_handler.apply_spell_effect(talent_id)
        elif 2 in [talent_info[DB.spell_column_info["Effect1"]],  # TODO also add pure dots to dmg spells
                   talent_info[DB.spell_column_info["Effect2"]],
                   talent_info[DB.spell_column_info["Effect3"]]]:
            self.char[char_index].damage_spells.append(talent_id)
        elif talent_id in self.mage_boost_spells:
            self.char[char_index].boost_spells.append(talent_id)
        elif talent_id in self.mage_mana_spells:
            self.char[char_index].mana_spells.append(talent_id)
        else:
            self.char[char_index].defensive_spells.append(talent_id)

    def load_item_sets(self, char_index):
        item_set_items = {}
        for item in self.char[char_index].gear.values():
            if item.item_data[DB.item_column_info["itemset"]] != 0:
                item_set_id = item.item_data[DB.item_column_info["itemset"]]
                if item_set_id in item_set_items.keys():
                    item_set_items[item_set_id].append(item.item_data[0])
                else:
                    item_set_items[item_set_id] = [item.item_data[0]]

        for item_set_info in item_set_items.items():
            item_set_data = DB.get_item_set(item_set_info[0])
            set_pieces = len(item_set_info[1])
            for i in range(1, 9):
                if set_pieces >= item_set_data[DB.item_set_column_info["pieces_" + str(i)]] != 0:
                    self.char[char_index].combat_handler.apply_spell_effect(
                        item_set_data[DB.item_set_column_info["bonus_" + str(i)]])

    def load_character_items(self, char_index, gear_settings):
        meta_gems_to_check = []
        for item in gear_settings.items():
            if item[1] is not None:
                item_from_db = DB.get_item(int(item[1]["item_id"]))

                if item_from_db is not None:
                    self.load_character_item(char_index, item[0], item_from_db)
                else:
                    ValueError("Item " + str(item[1]["item_id"]) + " in Inventory Slot " + str(item[0]) + " not found")

                if "enchant" in item[1]:
                    enchantment = DB.get_enchant(item[1]["enchant"])
                    self.char[char_index].gear[item[0]].enchantment = enchantment[
                        DB.enchant_column_info["m_name_lang_1"]]
                    self.apply_enchantment(char_index, enchantment)

                if "gems" in item[1]:
                    for gem_socket in item[1]["gems"]:
                        gem_item_info = DB.get_item(item[1]["gems"][gem_socket])
                        gem_info = DB.get_gem(gem_item_info[DB.item_column_info["GemProperties"]])
                        gem_enchant_info = DB.get_enchant(gem_info[1])
                        item_socket = self.char[char_index].gear[item[0]].sockets[gem_socket - 1]
                        item_socket[1] = gem_info[4]
                        item_socket[2] = gem_item_info[DB.item_column_info["name"]]
                        item_socket[3] = gem_enchant_info[DB.enchant_column_info["m_name_lang_1"]]
                        if item_socket[1] & 1:
                            meta_gems_to_check.append([item_socket, gem_enchant_info])
                        else:
                            self.apply_enchantment(char_index, gem_enchant_info)
                    self.check_gem_socket_bonus(char_index, item[0])
        self.load_item_sets(char_index)
        self.check_meta_gem_conditions(char_index, meta_gems_to_check)

    def check_meta_gem_conditions(self, char_index, meta_gems):
        for gem_to_check in meta_gems:
            if self.meta_gem_condition(char_index, gem_to_check[1][DB.enchant_column_info["m_condition_id"]]):
                self.apply_enchantment(char_index, gem_to_check[1])
                gem_to_check[0][4] = True
            else:
                gem_to_check[0][4] = False

    def meta_gem_condition(self, char_index, condition_id):
        condition_info = DB.get_enchant_condition(condition_id)
        gem_conditions = []
        for i in range(1, 6):
            gemtype = condition_info[DB.enchant_condition_column_info["m_lt_operandType" + str(i)]]
            if gemtype:
                operator = condition_info[DB.enchant_condition_column_info["m_operator" + str(i)]]
                value = condition_info[DB.enchant_condition_column_info["m_rt_operand" + str(i)]]
                gem_conditions.append([enums.socket_bitmask[gemtype], operator, value])

        for gem_condition in gem_conditions:
            typecounter = 0
            for item in self.char[char_index].gear.values():
                for socket in item.sockets:
                    if socket[1] and socket[1] & gem_condition[0]:
                        typecounter += 1

            if gem_condition[1] == 5:
                if typecounter < gem_condition[2]:
                    return False
            elif gem_condition[1] == 2:
                if typecounter >= gem_condition[2]:
                    return False
            elif gem_condition[1] == 3:
                if typecounter <= gem_condition[2]:
                    return False
        return True

    def check_gem_socket_bonus(self, char_index, inventory_slot):
        sockets_match = True
        for socket in self.char[char_index].gear[inventory_slot].sockets:
            if not socket[0] or not socket[1] or not socket[0] & socket[1]:
                sockets_match = False
        self.char[char_index].gear[inventory_slot].socket_bonus_met = sockets_match
        if sockets_match:
            self.apply_enchantment(char_index, DB.get_enchant(self.char[char_index].gear[inventory_slot].socket_bonus))

    def apply_enchantment(self, char_index, enchantment_info):
        for effect_slot in range(1, 4):
            # 1: combat spell
            if enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 1:
                pass
            # 2: damage
            elif enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 2:
                pass
            # 3: apply spell
            elif enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 3:
                try:
                    self.char[char_index].combat_handler.apply_spell_effect(
                        enchantment_info[DB.enchant_column_info["m_effectArg" + str(effect_slot)]])
                except NotImplementedWarning as e:
                    self.sim_results.errors.append(str(e))
            # 4: resistance mod
            elif enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 4:
                pass
            # 5: stat modification
            elif enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 5:
                try:
                    self.char[char_index].modify_stat(
                        enchantment_info[DB.enchant_column_info["m_effectArg" + str(effect_slot)]],
                        self.enchant_effect_strength(enchantment_info, effect_slot))
                except NotImplementedWarning as e:
                    self.sim_results.errors.append(str(e))
            # 6: totem
            elif enchantment_info[DB.enchant_column_info["m_effect" + str(effect_slot)]] == 6:
                pass

    @staticmethod
    def enchant_effect_strength(enchantment, effect_slot):
        return random.randint(enchantment[DB.enchant_column_info["m_effectPointsMin" + str(effect_slot)]],
                              enchantment[DB.enchant_column_info["m_effectPointsMax" + str(effect_slot)]])

    def load_character_item(self, char_index, inventory_slot, item_from_db):
        self.char[char_index].gear[inventory_slot] = EquippedItem(name=item_from_db[DB.item_column_info["name"]],
                                                                  item_data=item_from_db)

        for i in range(1, 11):
            stat_id = item_from_db[DB.item_column_info["stat_type" + str(i)]]
            stat_value = item_from_db[DB.item_column_info["stat_value" + str(i)]]
            if stat_value != 0:
                try:
                    self.char[char_index].modify_stat(stat_id, stat_value)
                except NotImplementedWarning as e:
                    self.sim_results.errors.append(str(e))

        for i in range(1, 6):
            spell_id = item_from_db[DB.item_column_info["spellid_" + str(i)]]
            if spell_id != 0:
                spell_trigger = item_from_db[DB.item_column_info["spelltrigger_" + str(i)]]

                # Item Spell Trigger "on use"
                if spell_trigger == 0:
                    self.char[char_index].active_consumables[item_from_db[0]] = 0
                # Item Spell Trigger "on equip"
                elif spell_trigger == 1:
                    try:
                        self.char[char_index].combat_handler.apply_spell_effect(spell_id)
                    except NotImplementedWarning as e:
                        self.sim_results.errors.append(str(e))
                # Item Spell Trigger "on hit"
                elif spell_trigger == 2:
                    # TODO: Implement
                    pass

        for i in range(1, 4):
            socket_color = item_from_db[DB.item_column_info["socketColor_" + str(i)]]
            if socket_color:
                self.char[char_index].gear[inventory_slot].sockets.append([socket_color, None, None, None, None])

        self.char[char_index].gear[inventory_slot].socket_bonus = item_from_db[DB.item_column_info["socketBonus"]]

    def get_sim_results(self):
        return self.sim_results

    def get_char_settings(self):
        return copy.deepcopy(self.char)

    def get_sim_settings(self):
        return copy.deepcopy(self.simSettings)
