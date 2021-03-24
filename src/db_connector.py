from functools import lru_cache

import mysql.connector
import logging

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


@lru_cache
def get_enchant(enchantment_id):
    try:
        tbcdb_cursor.execute("SELECT * FROM simdata.dbc_spellitemenchantment WHERE m_ID={}".format(enchantment_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during enchantment retrieval: {}".format(ex))


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


def get_class_talents(class_id, talent_index, talent_rank):
    try:
        tbcdb_cursor.execute(class_talent_query.format(talent_rank, class_id, talent_index))
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during class talent retrieval: {}".format(ex))


def get_item_set(item_set_id):
    try:
        tbcdb_cursor.execute(
            "SELECT * FROM simdata.dbc_itemset WHERE itemsetid={}".format(item_set_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during item set retrieval: {}".format(ex))


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
