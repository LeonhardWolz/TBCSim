import logging
import src.db_connector as DB


class Player(object):
    time_padding = 1

    def __init__(self, env, char, results):
        self.env = env
        self.char = char
        self.results = results
        self.logger = logging.getLogger("simulation")

    def rotation(self):
        self.logger.info("{:8s} {}".format("Simtime", "Current Action"))

        while True:
            self.char.spell_handler.remove_expired_auras()
            while self.env.now < self.char.gcd_end_time:
                yield self.env.timeout(1)

            spell_id = self.get_spell_to_cast()

            if self.char.can_cast_spell(spell_id):
                yield self.env.process(self.cast_spell(spell_id))
            else:
                self.logg("Can't cast " + DB.get_spell_name(spell_id) + ". Idleing for 0.5s")
                yield self.env.timeout(500)

            yield self.env.timeout(self.time_padding)

    def get_spell_to_cast(self):
        #return 30451
        # TODO Implement next spell
        if self.env.now == 0:
            return 11129
        else:
            return 38692
            #return 27079
            #return 38697

    def mana_regeneration(self):
        while True:
            if self.char.is_casting:
                self.char.current_mana += int(self.char.mp5_while_casting() * 0.4)
            else:
                self.char.current_mana += int(self.char.mp5_not_casting() * 0.4)
            yield self.env.timeout(2000)

    def five_second_rule(self):
        self.char.five_second_casting_counter += 1
        yield self.env.timeout(5000)
        self.char.five_second_casting_counter -= 1

    def curr_sim_time_str(self):
        return str(self.env.now / 1000)

    def logg(self, info):
        self.logger.info("{:8s} {}".format(self.curr_sim_time_str(), info))

    def cast_spell(self, spell_id):
        self.logg("Begin Cast " + DB.get_spell_name(spell_id))
        self.start_gcd(spell_id)
        yield self.env.timeout(self.char.spell_cast_time(spell_id))
        self.env.process(self.five_second_rule())
        self.five_second_rule()
        self.results.spell_cast(spell_id)
        self.char.cast_mana_spell(spell_id)
        self.char.spell_handler.apply_spell_effect(spell_id)

    def start_gcd(self, spell_id):
        self.char.gcd_end_time = self.env.now + self.char.get_spell_gcd(spell_id)
