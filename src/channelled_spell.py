import logging


class ChannelledSpell(object):
    def __init__(self, channel_type, env, spell_handler, spell_id, interval, duration, results, trigger_spell=None):
        self.channel_type = channel_type
        self.env = env
        self.spell_handler = spell_handler
        self.spell_id = spell_id
        self.interval = interval
        self.duration = duration
        self.results = results
        self.trigger_spell = trigger_spell
        self.logger = logging.getLogger("simulation")
        self.start = env.now

    def channel(self):
        while self.env.now <= self.duration + self.start:
            if self.channel_type == 23:
                self.spell_handler.apply_spell_effect(self.trigger_spell)
            yield self.env.timeout(self.interval)
