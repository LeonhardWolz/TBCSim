import mysql.connector
import logging

spell_cache = {}
spell_affected_cache = {}
tbcdb_cursor = None


def create_helper_dicts():
    i = 0
    for x in get_item_columns():
        item_column_info[x[0]] = i
        i += 1

    i = 0
    for x in get_spell_columns():
        spell_column_info[x[0]] = i
        i += 1


def get_spell_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"spell_template\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during spell column name retrieval: {}".format(ex))


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


def get_spell_name(spell_id):
    if spell_id in spell_cache.keys():
        return spell_cache[spell_id][spell_column_info["SpellName"]]
    else:
        try:
            tbcdb_cursor.execute("SELECT SpellName FROM simdata.spell_template WHERE id={}".format(spell_id))
            return str(tbcdb_cursor.fetchone()[0])
        except mysql.connector.Error as ex:
            logging.critical("DB Error during spell name retrieval: {}".format(ex))


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


def get_item_columns():
    try:
        tbcdb_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                             "WHERE TABLE_SCHEMA = \"simdata\" AND TABLE_NAME = \"item_template\"")
        return tbcdb_cursor.fetchall()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during item column name retrieval: {}".format(ex))


def get_equippable_item(item_id):
    try:
        tbcdb_cursor.execute(
            "SELECT * FROM simdata.item_template WHERE entry={} and (class = 2 or class = 4)".format(item_id))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during item retrieval: {}".format(ex))


def get_base_stats(player_class, race):
    try:
        tbcdb_cursor.execute(base_stats.format(player_class, race))
        return tbcdb_cursor.fetchone()
    except mysql.connector.Error as ex:
        logging.critical("DB Error during base stats retrieval: {}".format(ex))


def good_startup():
    if tbcdb_cursor is None:
        return False
    else:
        return True


base_stats = "select 	* " \
             "from 	tbcmangos.player_classlevelstats, " \
             "tbcmangos.player_levelstats " \
             "where 	tbcmangos.player_classlevelstats.class=tbcmangos.player_levelstats.class and " \
             "tbcmangos.player_levelstats.level = tbcmangos.player_classlevelstats.level and " \
             "tbcmangos.player_classlevelstats.level = 70 and " \
             "tbcmangos.player_levelstats.class = {} and " \
             "tbcmangos.player_levelstats.race = {}"

item_column_info = {}

spell_column_info = {}

try:
    tbcdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    tbcdb_cursor = tbcdb.cursor(buffered=True)
    create_helper_dicts()
except mysql.connector.Error as err:
    logging.critical("DB Error during startup: {}".format(err))
