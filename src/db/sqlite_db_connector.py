import sqlite3
import logging
from functools import lru_cache

from src import enums

BASE_STAT_QUERY = "select 	* " \
                  "from 	player_classlevelstats, player_levelstats " \
                  "where 	player_classlevelstats.class=player_levelstats.class and " \
                  "player_levelstats.level = player_classlevelstats.level and " \
                  "player_classlevelstats.level = 70 and " \
                  "player_levelstats.class = {} and " \
                  "player_levelstats.race = {}"

item_column_info = {}
spell_column_info = {}
item_set_column_info = {}
enchant_column_info = {}
enchant_condition_column_info = {}


def create_helper_dicts():
    for i, row in enumerate(get_item_columns()):
        item_column_info[row[1]] = i

    for i, row in enumerate(get_spell_columns()):
        spell_column_info[row[1]] = i

    for i, row in enumerate(get_item_set_columns()):
        item_set_column_info[row[1]] = i

    for i, row in enumerate(get_enchant_columns()):
        enchant_column_info[row[1]] = i

    for i, row in enumerate(get_enchant_condition_columns()):
        enchant_condition_column_info[row[1]] = i


def get_spell_columns():
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(spell_template)")
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell column name retrieval: {}".format(ex))


def get_item_columns():
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(item_template)")
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during item column name retrieval: {}".format(ex))


def get_item_set_columns():
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(dbc_itemset)")
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during itemset column name retrieval: {}".format(ex))


def get_enchant_columns():
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(dbc_spellitemenchantment)")
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during enchant column name retrieval: {}".format(ex))


def get_enchant_condition_columns():
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(dbc_spellitemenchantmentcondition)")
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during enchant condition column name retrieval: {}".format(ex))


@lru_cache(maxsize=None)
def get_spell(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM spell_template WHERE id={}".format(spell_id))
        value = cursor.fetchone()
        return tuple(value) if value else None
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell retrieval: {}".format(ex))


@lru_cache
def get_spell_name(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SpellName FROM spell_template WHERE id={}".format(spell_id))
        return str(cursor.fetchone()[0])
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell name retrieval: {}".format(ex))


@lru_cache
def get_spell_school(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SchoolMask FROM spell_template WHERE id={}".format(spell_id))
        return cursor.fetchone()[0]
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell school mask retrieval: {}".format(ex))


@lru_cache
def get_spell_family(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SpellFamilyFlags FROM spell_template WHERE id={}".format(spell_id))
        return cursor.fetchone()[0]
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell family mask retrieval: {}".format(ex))


@lru_cache
def get_spell_proc_info(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SchoolMask, SpellFamilyName, procFlags, procEx, ppmRate, CustomChance, Cooldown "
                       "FROM spell_proc_event WHERE entry={}".format(spell_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell proc event retrieval: {}".format(ex))


@lru_cache
def get_spell_gcd(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT StartRecoveryTime FROM spell_template WHERE id={}".format(spell_id))
        return cursor.fetchone()[0]
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell gcd retrieval: {}".format(ex))


@lru_cache
def get_spell_family_affected(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM spell_affect WHERE entry={}".format(spell_id))
        return cursor.fetchall()
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell affected family retrieval: {}".format(ex))


@lru_cache
def get_spell_is_passive(spell_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Attributes FROM spell_template WHERE id={}".format(spell_id))
        return True if cursor.fetchone()[0] & 0x00000040 == 64 else False
    except sqlite3.Error as ex:
        logging.critical("DB Error during spell passive flag retrieval: {}".format(ex))


@lru_cache
def get_item(item_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM item_template WHERE entry={}".format(item_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during item retrieval: {}".format(ex))


@lru_cache
def get_item_name(item_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM item_template WHERE entry={}".format(item_id))
        return str(cursor.fetchone()[0])
    except sqlite3.Error as ex:
        logging.critical("DB Error during item name retrieval: {}".format(ex))
        raise ValueError


@lru_cache
def get_enchant(enchantment_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbc_spellitemenchantment WHERE m_ID={}".format(enchantment_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during enchantment retrieval: {}".format(ex))


@lru_cache
def get_enchant_name(enchantment_id):
    cursor = conn.cursor()
    try:
        query = "Select SpellName " \
                "FROM spell_template " \
                f"WHERE Effect1=53 and EffectMiscValue1={enchantment_id}"
        cursor.execute(query)
        return str(cursor.fetchone()[0])
    except sqlite3.Error as ex:
        logging.critical("DB Error during enchantment name retrieval: {}".format(ex))


@lru_cache
def get_enchant_condition(condition_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbc_spellitemenchantmentcondition WHERE m_ID={}".format(condition_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during enchantment condition retrieval: {}".format(ex))


@lru_cache
def get_gem(gem_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbc_gemproperties WHERE id={}".format(gem_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during gem retrieval: {}".format(ex))


def get_base_stats(player_class, race):
    cursor = conn.cursor()
    try:
        cursor.execute(BASE_STAT_QUERY.format(player_class, race))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during base stats retrieval: {}".format(ex))


@lru_cache
def get_talent_tab_id(player_class_id, tab_pos):
    cursor = conn.cursor()
    try:
        cursor.execute(f"select id from dbc_talenttab "
                       f"where class_mask&(1<<({player_class_id}-1)) and tab_pos={tab_pos}")
        return cursor.fetchone()[0]
    except sqlite3.Error as ex:
        logging.critical("DB Error during talent tab id retrieval: {}".format(ex))


@lru_cache
def get_talent_id(talent_tab_id, talent_index, talent_rank):
    cursor = conn.cursor()
    try:
        cursor.execute(f"select rank{talent_rank} from dbc_talent "
                       f"where tab={talent_tab_id} order by row, col")
        return cursor.fetchall()[talent_index][0]
    except sqlite3.Error as ex:
        logging.critical("DB Error during talent retrieval: {}".format(ex))


def get_item_set(item_set_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbc_itemset WHERE itemsetid={}".format(item_set_id))
        return cursor.fetchone()
    except sqlite3.Error as ex:
        logging.critical("DB Error during item set retrieval: {}".format(ex))


@lru_cache
def get_gui_spell_dict():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Id, SpellName, Rank1 FROM spell_template where SpellFamilyFlags != 0")
        spell_dict = {}
        for result in cursor.fetchall():
            spell_dict[result[0]] = (result[1] + " " + (result[2] or ""),)
        return spell_dict
    except sqlite3.Error as ex:
        logging.critical("DB Error during gui spell list retrieval: {}".format(ex))


@lru_cache
def get_gui_consumable_dict():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT entry, name FROM item_template where class=0")
        consumable_dict = {}
        for result in cursor.fetchall():
            consumable_dict[result[0]] = (result[1],)
        return consumable_dict
    except sqlite3.Error as ex:
        logging.critical("DB Error during gui consumable list retrieval: {}".format(ex))


@lru_cache
def get_gui_gem_dict():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT entry, name, m_name_lang_1"
                       " FROM"
                       " (SELECT entry, name, GemProperties, id, SpellItemEnchantment, m_ID, m_name_lang_1"
                       " FROM item_template, dbc_gemproperties, dbc_spellitemenchantment"
                       " WHERE GemProperties!=0 AND GemProperties=id AND SpellItemEnchantment=m_ID) as gems")
        gem_dict = {}
        for result in cursor.fetchall():
            gem_dict[result[0]] = (result[1], result[2])
        return gem_dict
    except sqlite3.Error as ex:
        logging.critical("DB Error during gui gem list retrieval: {}".format(ex))


@lru_cache
def get_gui_enchantments_dict(item_class, item_subclass_mask=0, inventory_type_mask=0):
    cursor = conn.cursor()
    my_where_statement = ""

    if item_class == 4:
        my_where_statement = f" and EquippedItemInventoryTypeMask&{inventory_type_mask}"
    elif item_class == 2:
        my_where_statement = f" and EquippedItemClass=2 and EquippedItemSubClassMask&{item_subclass_mask}"

    query = "SELECT m_ID as Id, SpellName as Name, m_name_lang_1 as Description FROM " \
            "(SELECT Id, m_ID, EffectMiscValue1, SpellName, m_name_lang_1 " \
            "FROM spell_template, dbc_spellitemenchantment " \
            f"WHERE Effect1=53 and m_ID=EffectMiscValue1 {my_where_statement}) as Enchants"

    try:
        cursor.execute(query)
        enchants_dict = {}
        for result in cursor.fetchall():
            enchants_dict[result[0]] = (result[1], result[2])
        return enchants_dict
    except sqlite3.Error as ex:
        logging.critical("DB Error during gui enchantment list retrieval: {}".format(ex))


def get_item_can_be_enchanted(item_class, item_subclass_mask, inventory_type_mask):
    cursor = conn.cursor()
    my_where_statement = ""
    if item_class == 4:
        my_where_statement = f" and EquippedItemInventoryTypeMask&{inventory_type_mask}"
    elif item_class == 2:
        my_where_statement = f" and EquippedItemClass={item_class} and EquippedItemSubClassMask&{item_subclass_mask}"

    query = f"SELECT COUNT(*) FROM spell_template WHERE Effect1=53 {my_where_statement}"
    try:
        cursor.execute(query)
        for result in cursor.fetchall():
            if result[0] == 0:
                return False
            else:
                return True
    except sqlite3.Error as ex:
        logging.critical("DB Error during item can be enchanted retrieval: {}".format(ex))


@lru_cache
def get_gear_items_for_slot(inv_slot):
    cursor = conn.cursor()
    query_str = "SELECT entry, name FROM item_template"
    for index, inv_type in enumerate(enums.inv_type_in_slot[inv_slot]):
        if index == 0:
            query_str += " where ("
        else:
            query_str += " or"
        query_str += " InventoryType=" + str(inv_type)

    # add filter for placeholder items in slots with durability
    if inv_slot not in (0, 2, 4, 11, 12, 13, 14, 15, 19):
        query_str += ") and ItemLevel != 0"
    else:
        query_str += ")"

    try:
        cursor.execute(query_str)
        gear_dict = {}
        for result in cursor.fetchall():
            gear_dict[result[0]] = (result[1],)
        return gear_dict
    except sqlite3.Error as ex:
        logging.critical("DB Error during gear item retrieval: {}".format(ex))


conn = None
try:
    conn = sqlite3.connect("../data/database/database.db", check_same_thread=False)
    create_helper_dicts()
except sqlite3.Error as e:
    logging.critical("DB Error during startup: {}".format(e))
