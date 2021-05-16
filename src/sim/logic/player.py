import src.db.db_connector as DB
from src import enums
from src.enums import CombatAction
from src.sim.logic.combat_raters.fire_mage_car import FireMageCAR
from src.sim.logic.combat_raters.mage_car import MageCAR

combat_action_raters = {
    "Default": MageCAR,
    "FireMageCAR": FireMageCAR
}


class Player(object):
    time_padding = 1
    max_spell_damage = 0

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
            self.char.spell_handler.remove_expired_auras()
            self.char.spell_handler.recover_cooldowns()
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
                self.consume_item(combat_action[1])

            yield self.env.timeout(self.time_padding)

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
        self.results.logg("{:8s} {}".format(self.curr_sim_time_str(), info))

    def cast_spell(self, spell_id):
        spell_duration_index = DB.get_spell(spell_id)[DB.spell_column_info["DurationIndex"]]
        spell_duration = enums.duration_index[spell_duration_index if spell_duration_index != 0 else 1]
        spell_cast_time = self.char.spell_cast_time(spell_id)

        if spell_cast_time != 0:
            self.logg("Begin Cast " + DB.get_spell_name(spell_id) + " " +
                      DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]])
        elif DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 4 or \
                DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 64:
            self.logg("Begin Channel " + DB.get_spell_name(spell_id) + " " +
                      DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]])
        else:
            self.logg("Cast " + DB.get_spell_name(spell_id) + " " +
                      DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]])

        self.start_gcd(spell_id)
        yield self.env.timeout(spell_cast_time)

        if spell_cast_time != 0 and (not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 4 and
                                     not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 64):
            self.logg("Cast Completed " + DB.get_spell_name(spell_id) + " " +
                      DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]])

        self.env.process(self.five_second_rule())
        if not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 4 and \
                not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 64:
            self.results.spell_cast(spell_id, self.env.now)

        self.char.cast_mana_spell(spell_id)
        self.char.spell_handler.spell_start_cooldown(spell_id)
        self.env.process(self.char.spell_handler.apply_spell_effect_delay(spell_id))

        if DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 4 or \
                DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 64:
            yield self.env.timeout(spell_duration if spell_duration >= 0 else 0)

    def wand_attack(self):
        self.logg("Start Wand attack with " + self.char.gear[18].name)
        yield self.env.timeout(self.char.weapon_attack_delay_time(18))
        self.results.wand_attack_used(self.char.gear[18].item_data[0], self.env.now)
        self.char.spell_handler.process_wand_attack()

    def start_gcd(self, spell_id):
        self.char.gcd_end_time = self.env.now + self.char.get_spell_gcd(spell_id)

    def consume_item(self, item_id):
        item_info = DB.get_item(item_id)
        self.results.item_used(item_id, self.env.now)
        self.logg("Used " + item_info[DB.item_column_info["name"]])
        for i in range(1, 6):
            item_spell_id = item_info[DB.item_column_info["spellid_" + str(i)]]
            if item_spell_id:
                self.char.spell_handler.apply_spell_effect(item_spell_id, item_id)
                self.char.spell_handler.item_start_cooldown(item_id)

                self.char.active_consumables[item_id] += 1
                # remove some active items after charges used eg. mana gems
                if item_info[DB.item_column_info["spellcharges_" + str(i)]] \
                        + self.char.active_consumables[item_id] == 0 \
                        and item_info[DB.item_column_info["spellcategory_" + str(i)]] == 1153:
                    del self.char.active_consumables[item_id]
