import src.db.sqlite_db_connector as DB


class DotSpell(object):
    def __init__(self, env, spell_handler, spell_id, dot_dmg, interval, duration, results):
        self.env = env
        self.spell_handler = spell_handler
        self.spell_id = spell_id
        self.dot_dmg = dot_dmg
        self.interval = interval
        self.duration = duration
        self.results = results
        self.start = env.now

    def ticking(self):
        spell_from_db = DB.get_spell(self.spell_id)
        # normal hit
        self.results.dot_spell_hit(self.spell_id,
                                   spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                                   (spell_from_db[DB.spell_column_info["Rank1"]] or ""))
        while self.env.now <= self.duration + self.start:
            self.spell_handler.logg(spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                                    (spell_from_db[DB.spell_column_info["Rank1"]] or "") + " " +
                                    str(self.start / 1000) + " Dot damage: " + str(self.dot_dmg))
            self.results.dot_spell_damage(self.spell_id,
                                          spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                                          (spell_from_db[DB.spell_column_info["Rank1"]] or ""),
                                          self.dot_dmg)
            yield self.env.timeout(self.interval)
