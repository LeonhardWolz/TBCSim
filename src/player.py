import logging

import src.db_connector as DB
from src.enums import CombatAction


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
            self.char.spell_handler.recover_cooldowns()
            while self.env.now < self.char.gcd_end_time:
                yield self.env.timeout(1)

            combat_action = self.get_next_combat_action()

            if combat_action[0] == CombatAction.Idle:
                self.logg("Idleing for 0.5s")
                yield self.env.timeout(500)
            elif combat_action[0] == CombatAction.Cast_Spell:
                yield self.env.process(self.cast_spell(combat_action[1]))
            elif combat_action[0] == CombatAction.Wand_Attack:
                yield self.env.process(self.wand_attack())

            yield self.env.timeout(self.time_padding)

    def get_next_combat_action(self):
        misc_spell_action = self.get_misc_spell_action()
        if misc_spell_action is not None:
            return misc_spell_action

        damage_spell_action = self.get_damage_spell_action()
        if damage_spell_action is not None:
            return damage_spell_action

        if self.char.has_wand_range_attack():
            return [CombatAction.Wand_Attack]

        return [CombatAction.Idle]

    def get_misc_spell_action(self):
        # TODO implement more sophisticated logic to find best use for power spells
        for spell_id in self.char.usable_active_spells:
            if not self.char.spell_handler.spell_on_cooldown(spell_id):
                return [CombatAction.Cast_Spell, spell_id]

    def get_damage_spell_action(self):
        damage_spells_to_consider = []
        for spell_id in self.char.usable_damage_spells:
            if not self.char.spell_handler.spell_on_cooldown(spell_id) and self.char.has_mana_to_cast_spell(spell_id):
                damage_spells_to_consider.append({"spell_id": spell_id,
                                                  "spell_rating": self.get_spell_rating(spell_id)})

        damage_spells_to_consider.sort(key=lambda x: x["spell_rating"])

        if damage_spells_to_consider:
            return [CombatAction.Cast_Spell, damage_spells_to_consider.pop()["spell_id"]]
        else:
            return None

    def get_spell_rating(self, spell_id):
        spell_info = DB.get_spell(spell_id)

        spell_rating = 0
        for i in range(1, 4):
            if spell_info[DB.spell_column_info["Effect" + str(i)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] == 6:
                spell_base_damage = self.get_avg_effect_strength(spell_info, i)
                spell_spell_power = self.char.spell_spell_power(spell_id)
                spell_power_coefficient = self.char.spell_power_coefficient(spell_id, proc_auras=False)
                spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                          * self.char.spell_handler.enemy_damage_taken_mod(spell_info[0])

                spell_rating += round((spell_base_damage + spell_spell_power * spell_power_coefficient)
                                      * spell_damage_multiplier
                                      * self.char.spell_crit_dmg_multiplier(spell_id, proc_auras=False)
                                      * self.char.spell_crit_chance_spell(spell_id, proc_auras=False))
            elif spell_info[DB.spell_column_info["Effect" + str(i)]] == 6 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] in [6, 25] and \
                    spell_info[DB.spell_column_info["EffectApplyAuraName" + str(i)]] == 3:
                spell_base_damage = self.get_avg_effect_strength(spell_info, i)
                spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                          * self.char.spell_handler.enemy_damage_taken_mod(spell_info[0])

                spell_rating += round(spell_base_damage *
                                      spell_damage_multiplier)
        # TODO consider other effects
        # Damage Weight
        spell_rating *= 4

        spell_mana_cost = self.char.spell_resource_cost(spell_id, proc_auras=False)
        spell_mana_cost = spell_mana_cost if spell_mana_cost != 0 else 1

        cast_time = self.char.spell_cast_time(spell_id, proc_auras=False)

        normalized_cast_time = max(cast_time, 1500)

        # print(DB.get_spell_name(spell_id) + str(spell_id),
        #       spell_rating / (normalized_cast_time - spell_mana_cost))

        return spell_rating / (normalized_cast_time - spell_mana_cost)

    def get_avg_effect_strength(self, spell_info, effect_slot):
        min_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * 1
        max_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
                    spell_info[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
        return (min_value + max_value) / 2

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
        self.logg("Begin Cast " + DB.get_spell_name(spell_id) + " " +
                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]])
        self.start_gcd(spell_id)
        yield self.env.timeout(self.char.spell_cast_time(spell_id))
        self.env.process(self.five_second_rule())
        self.five_second_rule()
        self.results.spell_cast(spell_id, self.env.now)
        self.char.cast_mana_spell(spell_id)
        self.char.spell_handler.spell_start_cooldown(spell_id)
        self.char.spell_handler.apply_spell_effect(spell_id)

    def wand_attack(self):
        self.logg("Start Wand attack with " + self.char.items[18].name)
        yield self.env.timeout(self.char.weapon_attack_delay_time(18))
        self.results.wand_attack_used(self.char.items[18].item_data[0], self.env.now)
        self.char.spell_handler.process_wand_attack()

    def start_gcd(self, spell_id):
        self.char.gcd_end_time = self.env.now + self.char.get_spell_gcd(spell_id)
