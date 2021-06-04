import src.db.sqlite_db_connector as DB


class PeriodicTriggerAura(object):
    def __init__(self, env, spell_handler, trigger_spell_id, interval, duration):
        self.env = env
        self.spell_handler = spell_handler
        self.trigger_spell_id = trigger_spell_id
        self.interval = interval
        self.duration = duration
        self.start = env.now

    def processing(self):
        while self.duration == -1 or self.env.now <= self.duration + self.start:
            self.spell_handler.apply_spell_effect_delay(self.trigger_spell_id)
            yield self.env.timeout(self.interval)
