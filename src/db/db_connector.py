from functools import lru_cache

import mysql.connector
import logging

from src import enums

spell_cache = {}
spell_affected_cache = {}
item_cache = {}
tbcdb_cursor = None

base_stat_query = "select 	* " \
                  "from 	tbcmangos.player_classlevelstats, " \
                  "tbcmangos.player_levelstats " \
                  "where 	tbcmangos.player_classlevelstats.class=tbcmangos.player_levelstats.class and " \
                  "tbcmangos.player_levelstats.level = tbcmangos.player_classlevelstats.level and " \
                  "tbcmangos.player_classlevelstats.level = 70 and " \
                  "tbcmangos.player_levelstats.class = {} and " \
                  "tbcmangos.player_levelstats.race = {}"

class_talent_query = "SELECT talent_id_rank{}" \
                     " FROM simdata.class_talent_trees where class_id={} and talent_index={}"

item_column_info = {}
item_set_column_info = {}
spell_column_info = {}
enchant_column_info = {}
enchant_condition_column_info = {}


def create_helper_dicts():
    i = 0
    for x in get_item_columns():
        item_column_info[x[0]] = i
        i += 1

    i = 0
    for x in get_spell_columns():
        spell_column_info[x[0]] = i
        i += 1

    i = 0
    for x in get_item_set_columns():
        item_set_column_info[x[0]] = i
        i += 1

    i = 0
    for x in get_enchant_columns():
        enchant_column_info[x[0]] = i
        i += 1

    i = 0
    for x in get_enchant_condition_columns():
        enchant_condition_column_info[x[0]] = i
        i += 1


def get_spell_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"spell_template\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during spell column name retrieval: {}".format(ex))


def get_item_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"item_template\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during item column name retrieval: {}".format(ex))


def get_item_set_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"dbc_itemset\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during itemset column name retrieval: {}".format(ex))


def get_enchant_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"dbc_spellitemenchantment\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchant column name retrieval: {}".format(ex))


def get_enchant_condition_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"dbc_spellitemenchantmentcondition\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchant condition column name retrieval: {}".format(ex))


@lru_cache
def get_spell(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id]
    else:
        try:
            tbcdb_cursor.execute("SELECT * FROM simdata.spell_template WHERE id={}".format(spell_id))
            spell_info = tbcdb_cursor.fetchone()
            spell_cache[spell_id] = spell_info
            return spell_info
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell retrieval: {}".format(ex))


@lru_cache
def get_spell_name(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id][spell_column_info["SpellName"]]
    else:
        try:
            tbcdb_cursor.execute("SELECT SpellName FROM simdata.spell_template WHERE id={}".format(spell_id))
            return str(tbcdb_cursor.fetchone()[0])
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell name retrieval: {}".format(ex))


@lru_cache
def get_spell_school(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id][spell_column_info["SchoolMask"]]
    else:
        try:
            tbcdb_cursor.execute("SELECT SchoolMask FROM simdata.spell_template WHERE id={}".format(spell_id))
            return tbcdb_cursor.fetchone()[0]
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell school mask retrieval: {}".format(ex))


@lru_cache
def get_spell_family(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id][spell_column_info["SpellFamilyFlags"]]
    else:
        try:
            tbcdb_cursor.execute("SELECT SpellFamilyFlags FROM simdata.spell_template WHERE id={}".format(spell_id))
            return str(tbcdb_cursor.fetchone()[0])
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell family mask retrieval: {}".format(ex))


@lru_cache
def get_spell_gcd(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id][spell_column_info["StartRecoveryTime"]]
    else:
        try:
            tbcdb_cursor.execute("SELECT StartRecoveryTime FROM simdata.spell_template WHERE id={}".format(spell_id))
            return tbcdb_cursor.fetchone()
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell gcd retrieval: {}".format(ex))


def get_spell_family_affected(spell_id):
    if spell_id in spell_affected_cache.keys():
        return spell_affected_cache[spell_id]
    else:
        try:
            tbcdb_cursor.execute("SELECT * FROM simdata.spell_affect WHERE entry={}".format(spell_id))
            spell_affected_cache[spell_id] = tbcdb_cursor.fetchone()
            return spell_affected_cache[spell_id]
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell affected family retrieval: {}".format(ex))


def get_spell_is_passive(spell_id):
    if spell_id in spell_affected_cache.keys():
        return True if spell_affected_cache[spell_id][spell_column_info["Attributes"]] & 0x00000040 == 64 else False
    else:
        try:
            tbcdb_cursor.execute("SELECT Attributes FROM simdata.spell_template WHERE id={}".format(spell_id))
            return True if tbcdb_cursor.fetchone()[0] & 0x00000040 == 64 else False
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell passive flag retrieval: {}".format(ex))


@lru_cache
def get_item(item_id):
    if item_id in item_cache.keys():
        return item_cache[item_id]
    else:
        try:
            tbcdb_cursor.execute("SELECT * FROM simdata.item_template WHERE entry={}".format(item_id))
            item_cache[item_id] = tbcdb_cursor.fetchone()
            return item_cache[item_id]
        except mysql.connector.Error as ex:
            logging.critical("DB Error during item retrieval: {}".format(ex))


@lru_cache
def get_item_name(item_id):
    if item_id in item_cache.keys():
        return str(item_cache[item_id][item_column_info["name"]])
    else:
        try:
            tbcdb_cursor.execute("SELECT name FROM simdata.item_template WHERE entry={}".format(item_id))
            return str(tbcdb_cursor.fetchone()[0])
        except mysql.connector.Error as ex:
            logging.critical("DB Error during item name retrieval: {}".format(ex))
            raise ValueError


@lru_cache
def get_enchant(enchantment_id):
    try:
        tbcdb_cursor.execute("SELECT * FROM simdata.dbc_spellitemenchantment WHERE m_ID={}".format(enchantment_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchantment retrieval: {}".format(ex))


@lru_cache
def get_enchant_name(enchantment_id):
    try:
        query = "Select SpellName " \
                "FROM simdata.spell_template " \
                f"WHERE Effect1=53 and EffectMiscValue1={enchantment_id}"
        tbcdb_cursor.execute(query)
        return str(tbcdb_cursor.fetchone()[0])
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchantment name retrieval: {}".format(ex))


@lru_cache
def get_enchant_condition(condition_id):
    try:
        tbcdb_cursor.execute(
            "SELECT * FROM simdata.dbc_spellitemenchantmentcondition WHERE m_ID={}".format(condition_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchantment condition retrieval: {}".format(ex))


@lru_cache
def get_gem(gem_id):
    try:
        tbcdb_cursor.execute("SELECT * FROM simdata.dbc_gemproperties WHERE id={}".format(gem_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gem retrieval: {}".format(ex))


def get_base_stats(player_class, race):
    try:
        tbcdb_cursor.execute(base_stat_query.format(player_class, race))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during base stats retrieval: {}".format(ex))


#
# def get_class_talents(class_id, talent_index, talent_rank):
#     try:
#         tbcdb_cursor.execute(class_talent_query.format(talent_rank, class_id, talent_index))
#         return tbcdb_cursor.fetchall()
#     except mysql.connector.Error as ex:
#         logging.critical("DB Error during class talent retrieval: {}".format(ex))

@lru_cache
def get_talent_tab_id(player_class_id, tab_pos):
    try:
        tbcdb_cursor.execute(f"select id from simdata.dbc_talenttab "
                             f"where class_mask&1<<({player_class_id}-1) and tab_pos={tab_pos}")
        return tbcdb_cursor.fetchone()[0]
    except mysql.connector.Error as ex:
        logging.critical("DB Error during talent tab id retrieval: {}".format(ex))


@lru_cache
def get_talent_id(talent_tab_id, talent_index, talent_rank):
    try:
        tbcdb_cursor.execute(f"select rank{talent_rank} from simdata.dbc_talent "
                             f"where tab={talent_tab_id} order by row, col")
        return tbcdb_cursor.fetchall()[talent_index][0]
    except mysql.connector.Error as ex:
        logging.critical("DB Error during talent retrieval: {}".format(ex))


def get_item_set(item_set_id):
    try:
        tbcdb_cursor.execute(
            "SELECT * FROM simdata.dbc_itemset WHERE itemsetid={}".format(item_set_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during item set retrieval: {}".format(ex))


@lru_cache
def get_gui_spell_dict():
    try:
        tbcdb_cursor.execute("SELECT Id, SpellName, Rank1 FROM simdata.spell_template where SpellFamilyFlags != 0")
        spell_dict = {}
        for result in tbcdb_cursor.fetchall():
            spell_dict[result[0]] = (result[1] + " " + (result[2] or ""),)
        return spell_dict
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gui spell list retrieval: {}".format(ex))


@lru_cache
def get_gui_consumable_dict():
    try:
        tbcdb_cursor.execute("SELECT entry, name FROM simdata.item_template where class=0")
        consumable_dict = {}
        for result in tbcdb_cursor.fetchall():
            consumable_dict[result[0]] = (result[1],)
        return consumable_dict
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gui consumable list retrieval: {}".format(ex))


@lru_cache
def get_gui_gem_dict():
    try:
        tbcdb_cursor.execute("SELECT entry, name, m_name_lang_1"
                             " FROM"
                             " (SELECT entry, name, GemProperties, id, SpellItemEnchantment, m_ID, m_name_lang_1"
                             " FROM simdata.item_template, simdata.dbc_gemproperties, simdata.dbc_spellitemenchantment"
                             " WHERE GemProperties!=0 AND GemProperties=id AND SpellItemEnchantment=m_ID) as gems")
        gem_dict = {}
        for result in tbcdb_cursor.fetchall():
            gem_dict[result[0]] = (result[1], result[2])
        return gem_dict
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gui gem list retrieval: {}".format(ex))


@lru_cache
def get_gui_enchantments_dict(item_class, item_subclass_mask=0, inventory_type_mask=0):
    my_where_statement = ""

    if item_class == 4:
        my_where_statement = f" and EquippedItemInventoryTypeMask&{inventory_type_mask}"
    elif item_class == 2:
        my_where_statement = f" and EquippedItemClass=2 and EquippedItemSubClassMask&{item_subclass_mask}"

    query = "SELECT m_ID as Id, SpellName as Name, m_name_lang_1 as Description FROM " \
            "(SELECT Id, m_ID, EffectMiscValue1, SpellName, m_name_lang_1 " \
            "FROM simdata.spell_template, simdata.dbc_spellitemenchantment " \
            f"WHERE Effect1=53 and Rank1!=\"QASpell\" and m_ID=EffectMiscValue1 {my_where_statement}) as Enchants"

    try:
        tbcdb_cursor.execute(query)
        enchants_dict = {}
        for result in tbcdb_cursor.fetchall():
            enchants_dict[result[0]] = (result[1], result[2])
        return enchants_dict
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gui enchantment list retrieval: {}".format(ex))


@lru_cache
def get_gear_items_for_slot(inv_slot):
    query_str = "SELECT entry, name FROM simdata.item_template"
    for index, inv_type in enumerate(enums.inv_type_in_slot[inv_slot]):
        if index == 0:
            query_str += " where ("
        else:
            query_str += " or"
        query_str += " InventoryType=" + str(inv_type)

    # add filter for placeholder items in slots with durability
    if inv_slot not in (0, 2, 4, 11, 12, 13, 14, 15, 19):
        query_str += ") and ItemLevel != 0"
        # query_str += ") and MaxDurability != 0"
    else:
        query_str += ")"

    try:
        tbcdb_cursor.execute(query_str)
        gear_dict = {}
        for result in tbcdb_cursor.fetchall():
            gear_dict[result[0]] = (result[1],)
        return gear_dict
    except mysql.connector.Error as ex:
        logging.critical("DB Error during gear item retrieval: {}".format(ex))


def good_startup():
    if tbcdb_cursor is None:
        return False
    else:
        return True


try:
    tbcdb = mysql.connector.connect(
        pool_name="tbcsimpool",
        pool_size=5,
        host="localhost",
        user="root",
        password="root"
    )
    tbcdb_cursor = tbcdb.cursor(buffered=True)
    create_helper_dicts()
except mysql.connector.Error as err:
    logging.critical("DB Error during startup: {}".format(err))
