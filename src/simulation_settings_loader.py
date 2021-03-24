import re
from urllib.parse import urlparse

import yaml
import copy

from src import db_connector as DB
from src import enums
from src.enemy import Enemy

from src.sim_settings import SimSettings
from src.character import Character
from src.sim_results import EquippedItem

char = Character()
enemy = Enemy()
simSettings = SimSettings()

spells_to_use = {
    "Mage": "mage_spells_to_use"
}

mage_boost_spells = (11129, 12472)

mage_mana_spells = (12051,)


def load_settings():
    # load settings file
    with open('SimSettings.yml', 'r') as settings_yaml:
        cfg = yaml.safe_load(settings_yaml)

    # load sim settings
    load_sim_settings(cfg["simulation"])

    # load character settings
    load_character_settings(cfg["character"])

    # load enemy settings
    load_enemy_settings(cfg["enemy"])

    char.current_health = char.total_health
    char.current_mana = char.total_mana
    char.spell_handler.enemy = enemy


def load_sim_settings(sim_settings):
    simSettings.sim_type = sim_settings["sim_type"] if sim_settings["sim_type"] else "dps"
    simSettings.sim_duration = sim_settings["sim_duration"] * 1000 if sim_settings["sim_duration"] else 6000
    simSettings.sim_iterations = sim_settings["sim_iterations"] if sim_settings["sim_iterations"] else 1
    simSettings.results_file_path = sim_settings["results_file_path"] if sim_settings["results_file_path"] else None
    simSettings.full_log_for_best = sim_settings["full_log_for_best"] if sim_settings["full_log_for_best"] else False


def load_enemy_settings(enemy_settings):
    enemy.attributes["armor"] = enemy_settings["attributes"]["armor"]
    enemy.attributes["holy_resistance"] = enemy_settings["attributes"]["holy_resistance"]
    enemy.attributes["frost_resistance"] = enemy_settings["attributes"]["frost_resistance"]
    enemy.attributes["fire_resistance"] = enemy_settings["attributes"]["fire_resistance"]
    enemy.attributes["nature_resistance"] = enemy_settings["attributes"]["nature_resistance"]
    enemy.attributes["arcane_resistance"] = enemy_settings["attributes"]["arcane_resistance"]
    enemy.attributes["shadow_resistance"] = enemy_settings["attributes"]["shadow_resistance"]

    enemy.level = enemy_settings["level"]
    enemy.boss = enemy_settings["boss"]


def load_character_settings(char_settings):
    # load base stats for race and class specified in settings
    base_stats = DB.get_base_stats(enums.PlayerClass[char_settings["player_class"]].value,
                                   enums.Race[char_settings["race"]].value)

    char.modify_stat(1, base_stats[2])
    char.modify_stat(0, base_stats[3])
    char.modify_stat(4, base_stats[7])
    char.modify_stat(3, base_stats[8])
    char.modify_stat(7, base_stats[9])
    char.modify_stat(5, base_stats[10])
    char.modify_stat(6, base_stats[11])

    char.race = char_settings["race"]
    char.player_class = char_settings["player_class"]

    load_racials()
    load_class_spells(char_settings["spells"])

    load_consumables(char_settings)

    load_character_items(char_settings["gear"])
    load_talents(char_settings["talents"])


def load_racials():
    if char.race == "Human":
        char.spell_handler.apply_spell_effect(20598)
    elif char.race == "Orc":
        pass
    elif char.race == "Dwarf":
        char.spell_handler.apply_spell_effect(20595)
        char.spell_handler.apply_spell_effect(20596)
    elif char.race == "Nightelf":
        char.spell_handler.apply_spell_effect(20583)
    elif char.race == "Undead":
        char.spell_handler.apply_spell_effect(20579)
    elif char.race == "Tauren":
        char.spell_handler.apply_spell_effect(20551)
        char.spell_handler.apply_spell_effect(20550)
    elif char.race == "Gnome":
        char.spell_handler.apply_spell_effect(20592)
        char.spell_handler.apply_spell_effect(20591)
    elif char.race == "Troll":
        char.boost_spells.append(20554)
    elif char.race == "Bloodelf":
        char.spell_handler.apply_spell_effect(822)
    elif char.race == "Draenei":
        char.spell_handler.apply_spell_effect(6562)
        char.spell_handler.apply_spell_effect(28878)
        char.spell_handler.apply_spell_effect(20579)


def load_consumables(char_settings):
    for consumable_id in char_settings["passive_consumables"]:
        item_info = DB.get_item(consumable_id)
        for i in range(1, 4):
            spell_id = item_info[DB.item_column_info["spellid_" + str(i)]]
            if spell_id != 0:
                # bufffood triggers spell
                triggered_spell_id = char.spell_handler.spell_get_triggered_spell(spell_id)
                if triggered_spell_id != 0:
                    char.spell_handler.apply_spell_effect(triggered_spell_id)
                else:
                    char.spell_handler.apply_spell_effect(spell_id)
    if char_settings["active_consumables"]:
        for consumable_id in char_settings["active_consumables"]:
            char.active_consumables[consumable_id] = 0
    #
    # print(char.active_consumables)
    # for i, aura in enumerate(char.spell_handler.active_auras):
    #     print(i, aura)


def load_class_spells(spell_settings):
    for spell_id in spell_settings[spells_to_use.get(char.player_class)]:
        char.damage_spells.append(spell_id)

    for spell_id in spell_settings["passive_buffs"]:
        char.spell_handler.apply_spell_effect(spell_id)

    if char.player_class == "Mage":
        for spell_id in mage_mana_spells:
            char.mana_spells.append(spell_id)


def load_talents(talent_settings):
    if talent_settings["talent_calc_link"] is not None:
        talent_string = re.sub("tal=", "", urlparse(talent_settings["talent_calc_link"]).query)
        for num, talent in enumerate(talent_string, start=0):
            if int(talent) != 0:
                load_talent(DB.get_class_talents(getattr(enums.PlayerClass, char.player_class).value,
                                                 num,
                                                 talent)[0][0])

    elif talent_settings["talent_list"] is not None:
        for talent_id in talent_settings["talent_list"]:
            load_talent(talent_id)


def load_talent(talent_id):
    talent_info = DB.get_spell(talent_id)
    if talent_info[DB.spell_column_info["Attributes"]] & 0x00000040:
        char.spell_handler.apply_spell_effect(talent_id)
    elif 2 in [talent_info[DB.spell_column_info["Effect1"]],  # TODO also add pure dots to dmg spells
               talent_info[DB.spell_column_info["Effect2"]],
               talent_info[DB.spell_column_info["Effect3"]]]:
        char.damage_spells.append(talent_id)
    elif talent_id in mage_boost_spells:
        char.boost_spells.append(talent_id)
    elif talent_id in mage_mana_spells:
        char.mana_spells.append(talent_id)
    else:
        char.defensive_spells.append(talent_id)


def load_item_sets():
    item_set_items = {}
    for item in char.gear.values():
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
                char.spell_handler.apply_spell_effect(item_set_data[DB.item_set_column_info["bonus_" + str(i)]])


def load_character_items(gear_settings):
    meta_gems_to_check = []
    for item in gear_settings.items():
        if item[1] is not None:
            item_from_db = DB.get_item(int(item[1]["itemid"]))

            if item_from_db is not None:
                load_character_item(item[0], item_from_db)
            else:
                ValueError("Item " + str(item[1]["itemid"]) + " in Inventory Slot " + str(item[0]) + " not found")

            if "enchant" in item[1]:
                enchantment = DB.get_enchant(item[1]["enchant"])
                char.gear[item[0]].enchantment = enchantment[DB.enchant_column_info["m_name_lang_1"]]
                apply_enchantment(enchantment)

            if "gems" in item[1]:
                for gem_socket in item[1]["gems"]:
                    gem_item_info = DB.get_item(item[1]["gems"][gem_socket])
                    gem_info = DB.get_gem(gem_item_info[DB.item_column_info["GemProperties"]])
                    gem_enchant_info = DB.get_enchant(gem_info[1])
                    item_socket = char.gear[item[0]].sockets[gem_socket - 1]
                    item_socket[1] = gem_info[4]
                    item_socket[2] = gem_item_info[DB.item_column_info["name"]]
                    item_socket[3] = gem_enchant_info[DB.enchant_column_info["m_name_lang_1"]]
                    if item_socket[1] & 1:
                        meta_gems_to_check.append([item_socket, gem_enchant_info])
                    else:
                        apply_enchantment(gem_enchant_info)
                check_gem_socket_bonus(item[0])
    load_item_sets()
    check_meta_gem_conditions(meta_gems_to_check)


def check_meta_gem_conditions(meta_gems):
    for gem_to_check in meta_gems:
        if meta_gem_condition(gem_to_check[1][DB.enchant_column_info["m_condition_id"]]):
            apply_enchantment(gem_to_check[1])
            gem_to_check[0][4] = True
        else:
            gem_to_check[0][4] = False


def meta_gem_condition(condition_id):
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
        for item in char.gear.values():
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


def check_gem_socket_bonus(inventory_slot):
    sockets_match = True
    for socket in char.gear[inventory_slot].sockets:
        if not socket[0] or not socket[1] or not socket[0] & socket[1]:
            sockets_match = False
    char.gear[inventory_slot].socket_bonus_met = sockets_match
    if sockets_match:
        apply_enchantment(DB.get_enchant(char.gear[inventory_slot].socket_bonus))


def apply_enchantment(enchantment_info):
    for i in range(1, 4):
        if enchantment_info[DB.enchant_column_info["m_effect" + str(i)]] == 3:
            char.spell_handler.apply_spell_effect(enchantment_info[DB.enchant_column_info["m_effectArg" + str(i)]])


def load_character_item(inventory_slot, item_from_db):
    char.gear[inventory_slot] = EquippedItem(name=item_from_db[DB.item_column_info["name"]],
                                             item_data=item_from_db)

    for i in range(1, 11):
        stat_id = item_from_db[DB.item_column_info["stat_type" + str(i)]]
        stat_value = item_from_db[DB.item_column_info["stat_value" + str(i)]]
        if stat_value != 0:
            char.modify_stat(stat_id, stat_value)

    for i in range(1, 6):
        spell_id = item_from_db[DB.item_column_info["spellid_" + str(i)]]
        spell_trigger = item_from_db[DB.item_column_info["spelltrigger_" + str(i)]]
        if spell_id != 0 and spell_trigger == 1:
            char.spell_handler.apply_spell_effect(spell_id)

    for i in range(1, 4):
        socket_color = item_from_db[DB.item_column_info["socketColor_" + str(i)]]
        if socket_color:
            char.gear[inventory_slot].sockets.append([socket_color, None, None, None, None])

    char.gear[inventory_slot].socket_bonus = item_from_db[DB.item_column_info["socketBonus"]]


def get_settings():
    return copy.deepcopy(simSettings), copy.deepcopy(char)


def get_sim_settings():
    return copy.deepcopy(simSettings)
