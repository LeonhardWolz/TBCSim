import src.db.sqlite_db_connector as DB


class ChannelledSpell(object):
    def __init__(self, channel_type, env, spell_handler, spell_id, interval, duration, results, value=0):
        self.channel_aura = channel_type
        self.env = env
        self.spell_handler = spell_handler
        self.spell_id = spell_id
        self.interval = interval
        self.duration = duration
        self.results = results
        self.value = value
        self.start = env.now

    def channel(self):
        while self.env.now < self.duration + self.start:
            yield self.env.timeout(self.interval)
            if self.channel_aura == 21:
                mana_restore_amount = round(self.spell_handler.char.total_mana * (self.value / 100))
                self.spell_handler.logg("Gained " + str(mana_restore_amount)
                                        + " Mana from " + DB.get_spell_name(
                    self.spell_id))
                self.results.misc_effect(self.spell_id, mana_restore_amount)
                self.spell_handler.char.current_mana += mana_restore_amount
