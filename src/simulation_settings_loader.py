import yaml
import copy
import logging

from src import db_connector as DB
from src import enums
from src.enemy import Enemy

from src.sim_settings import SimSettings
from src.character import Character
from src.sim_results import EquippedItem

logger = logging.getLogger("simulation")

char = Character()
enemy = Enemy()
simSettings = SimSettings()

spells_to_use = {
    "Mage": "mage_spells_to_use"
}


def load_settings():
    # load settings file
    with open('SimSettings.yml', 'r') as settings_yaml:
        cfg = yaml.safe_load(settings_yaml)

    # load character settings
    load_character_settings(cfg["character"])

    # load enemy settings
    load_enemy_settings(cfg["enemy"])

    # load sim settings
    load_sim_settings(cfg["sim"])

    char.current_mana = char.total_mana
    char.spell_handler.enemy = enemy


def load_sim_settings(sim_settings):
    simSettings.sim_type = sim_settings["sim_type"]
    simSettings.duration = sim_settings["duration"] * 1000


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
    char.race = char_settings["race"]
    char.player_class = char_settings["player_class"]

    char.base_attributes["base_health"] = base_stats[2]
    char.base_attributes["base_mana"] = base_stats[3]
    char.base_attributes["base_strength"] = base_stats[7]
    char.base_attributes["base_agility"] = base_stats[8]
    char.base_attributes["base_stamina"] = base_stats[9]
    char.base_attributes["base_intellect"] = base_stats[10]
    char.base_attributes["base_spirit"] = base_stats[11]

    for spell_id in char_settings["spells"][spells_to_use.get(char.player_class)]:
        char.usable_spells.append(spell_id)

    load_character_items(char_settings["gear"])
    load_talents(char_settings["talents"])


def load_talents(talent_settings):
    if talent_settings is not None:
        for talent in talent_settings:
            char.spell_handler.apply_spell_effect(talent)


def load_character_items(gear_settings):
    for item in gear_settings.items():
        if item[1] is not None:
            item_from_db = DB.get_equippable_item(int(item[1]))

            if item_from_db is not None:
                load_character_item(item[0], item_from_db)
            else:
                logger.error("Item " + str(item[1]) + " in Inventory Slot " + str(item[0]) + " not found")


def load_character_item(inventory_slot, item_from_db):
    char.items[inventory_slot] = EquippedItem(item_from_db[DB.item_column_info["name"]], item_from_db)

    for i in range(1, 11):
        stat_id = item_from_db[DB.item_column_info["stat_type" + str(i)]]
        stat_value = item_from_db[DB.item_column_info["stat_value" + str(i)]]
        if stat_value != 0:
            try:
                char.modify_stat(stat_id, stat_value)
            except NotImplementedError as e:
                logger.error(str(e))
    for i in range(1, 6):
        spell_id = item_from_db[DB.item_column_info["spellid_" + str(i)]]
        spell_trigger = item_from_db[DB.item_column_info["spelltrigger_" + str(i)]]
        if spell_id != 0 and spell_trigger == 1:
            char.spell_handler.apply_spell_effect(spell_id)


def get_settings():
    return copy.deepcopy(simSettings), copy.deepcopy(char)
