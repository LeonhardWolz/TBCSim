
from src import enums
import src.db.sqlite_db_connector as DB
from src.enums import CombatAction
from src.sim.logic.combat_raters.fire_mage_car import FireMageCAR
from src.sim.logic.combat_raters.mage_car import MageCAR
from src.sim.logic.combat_raters.arcane_mage_car import ArcaneMageCAR

combat_action_raters = {
    "Default": MageCAR,
    "FireMageCAR": FireMageCAR,
    "ArcaneMageCAR": ArcaneMageCAR
}


class Player(object):
    time_padding = 1

    def __init__(self, env, char, results, rater):
        self.env = env
        self.char = char
        self.results = results
        try:
            self.combat_action_rater = combat_action_raters[rater](self)
        except KeyError:
            self.combat_action_rater = combat_action_raters["Default"](self)

    def rotation(self):
        self.results.logg("{:8s} {}".format("Simtime", "Current Action"))
        while True:
            self.char.combat_handler.remove_expired_auras()
            self.char.combat_handler.recover_cooldowns()
            while self.env.now < self.char.gcd_end_time:
                yield self.env.timeout(1)

            combat_action = self.combat_action_rater.get_next_combat_action()

            if combat_action[0] == CombatAction.Idle:
                self.logg("Idleing for 0.5s")
                yield self.env.timeout(500)
            elif combat_action[0] == CombatAction.Cast_Spell:
                yield self.env.process(self.cast_spell(combat_action[1]))
            elif combat_action[0] == CombatAction.Wand_Attack:
                yield self.env.process(self.wand_attack())
            elif combat_action[0] == CombatAction.Consume_Item:
                self.char.combat_handler.use_item(combat_action[1])

            yield self.env.timeout(self.time_padding)

    def mana_regeneration(self):
        while True:
            if self.char.is_casting:
                self.char.current_mana += self.char.mana_per_tick_while_casting()
            else:
                self.char.current_mana += self.char.mana_per_tick_not_casting()
            yield self.env.timeout(2000)

    def five_second_rule(self):
        self.char.five_second_casting_counter += 1
        yield self.env.timeout(5000)
        self.char.five_second_casting_counter -= 1

    def curr_sim_time_str(self):
        return str(self.env.now / 1000)

    def logg(self, info):
        self.results.logg("{:8s} {}".format(self.curr_sim_time_str(), info))

    def cast_spell(self, spell_id):
        spell_from_db = DB.get_spell(spell_id)
        spell_duration_index = spell_from_db[DB.spell_column_info["DurationIndex"]]
        spell_duration = enums.duration_index[spell_duration_index if spell_duration_index != 0 else 1]
        spell_cast_time = self.char.spell_cast_time(spell_id)

        if spell_cast_time != 0:
            self.logg("Begin Cast " + spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                      (spell_from_db[DB.spell_column_info["Rank1"]] or ""))
        elif spell_from_db[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_from_db[DB.spell_column_info["AttributesEx"]] & 64:
            self.logg("Begin Channel " + spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                      (spell_from_db[DB.spell_column_info["Rank1"]] or ""))
        else:
            self.logg("Cast " + spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                      (spell_from_db[DB.spell_column_info["Rank1"]] or ""))

        self.start_gcd(spell_id)
        yield self.env.timeout(spell_cast_time)

        if spell_cast_time != 0 and \
                (not spell_from_db[DB.spell_column_info["AttributesEx"]] & 4 and
                 not spell_from_db[DB.spell_column_info["AttributesEx"]] & 64):
            self.logg("Cast Completed " + spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                      (spell_from_db[DB.spell_column_info["Rank1"]] or ""))

        self.env.process(self.five_second_rule())
        if not spell_from_db[DB.spell_column_info["AttributesEx"]] & 4 and \
                not spell_from_db[DB.spell_column_info["AttributesEx"]] & 64:
            self.results.spell_cast(spell_id,
                                    spell_from_db[DB.spell_column_info["SpellName"]] + " " +
                                    (spell_from_db[DB.spell_column_info["Rank1"]] or ""),
                                    self.env.now)

        self.char.cast_mana_spell(spell_id)
        self.char.combat_handler.spell_start_cooldown(spell_id)
        self.env.process(self.char.combat_handler.apply_spell_effect_delay(spell_id))

        if spell_from_db[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_from_db[DB.spell_column_info["AttributesEx"]] & 64:
            yield self.env.timeout(spell_duration if spell_duration >= 0 else 0)

    def wand_attack(self):
        self.logg("Start Wand attack with " + self.char.gear[18].name)
        yield self.env.timeout(self.char.weapon_attack_delay_time(18))
        self.results.wand_attack_used(self.char.gear[18].item_data[0],
                                      self.char.gear[18].item_data[DB.item_column_info["name"]],
                                      self.env.now)
        self.char.combat_handler.process_wand_attack()

    def start_gcd(self, spell_id):
        self.char.gcd_end_time = self.env.now + self.char.get_spell_gcd(spell_id)

