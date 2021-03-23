from functools import lru_cache

import src.db_connector as DB
from src import enums
from src.enums import CombatAction


class Player(object):
    time_padding = 1
    max_spell_damage = 0

    def __init__(self, env, char, results):
        self.env = env
        self.char = char
        self.results = results

    def rotation(self):
        self.results.logg("{:8s} {}".format("Simtime", "Current Action"))
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
            elif combat_action[0] == CombatAction.Consume_Item:
                self.consume_item(combat_action[1])

            yield self.env.timeout(self.time_padding)

    def get_next_combat_action(self):
        misc_combat_action = self.get_misc_combat_action()
        if misc_combat_action is not None:
            return misc_combat_action

        boost_spell_action = self.get_boost_spell_action()
        if boost_spell_action is not None:
            return boost_spell_action

        damage_spell_action = self.get_damage_spell_action()
        if damage_spell_action is not None:
            return damage_spell_action

        if self.char.has_wand_range_attack():
            return [CombatAction.Wand_Attack]

        return [CombatAction.Idle]

    def get_misc_combat_action(self):
        misc_combat_actions_to_consider = []
        for spell_id in self.char.mana_spells:
            if not self.char.spell_handler.spell_on_cooldown(spell_id):
                misc_combat_actions_to_consider.append({"combat_action": [CombatAction.Cast_Spell, spell_id],
                                                        "combat_rating": self.get_mana_spell_rating(spell_id)})
        for item_id in self.char.active_consumables.keys():
            if not self.char.spell_handler.item_on_cooldown(item_id):
                misc_combat_actions_to_consider.append({"combat_action": [CombatAction.Consume_Item, item_id],
                                                        "combat_rating": self.get_consumable_rating(item_id)})

        misc_combat_actions_to_consider.sort(key=lambda x: x["combat_rating"])

        # print(self.char.current_mana, self.char.total_mana)
        # print(misc_combat_actions_to_consider)
        if misc_combat_actions_to_consider:
            misc_combat_action = misc_combat_actions_to_consider.pop()
            if misc_combat_action["combat_rating"] > 0:
                return misc_combat_action["combat_action"]

        return None

    def get_boost_spell_action(self):
        boost_spells_to_consider = []
        for spell_id in self.char.boost_spells:
            if not self.char.spell_handler.spell_on_cooldown(spell_id) and self.char.has_mana_to_cast_spell(spell_id):
                boost_spells_to_consider.append({"spell_id": spell_id,
                                                 "spell_rating": self.get_boost_spell_rating(spell_id)})

        boost_spells_to_consider.sort(key=lambda x: x["spell_rating"])
        # print(self.char.current_mana, self.char.total_mana)
        # print(boost_spells_to_consider)

        if boost_spells_to_consider:
            spell_to_consider = boost_spells_to_consider.pop()
            if spell_to_consider["spell_rating"] >= 0:
                return [CombatAction.Cast_Spell, spell_to_consider["spell_id"]]

        return None

    def get_damage_spell_action(self):
        damage_spells_to_consider = []
        for spell_id in self.char.damage_spells:
            if not self.char.spell_handler.spell_on_cooldown(spell_id) and self.char.has_mana_to_cast_spell(spell_id):
                damage_spells_to_consider.append({"spell_id": spell_id,
                                                  "spell_rating": self.get_offensive_spell_rating(spell_id)})

        damage_spells_to_consider.sort(key=lambda x: x["spell_rating"])

        if damage_spells_to_consider:
            spell_to_consider = damage_spells_to_consider.pop()
            if spell_to_consider["spell_rating"] > 0:
                return [CombatAction.Cast_Spell, spell_to_consider["spell_id"]]
            else:
                return None
        else:
            return None

    def get_mana_spell_rating(self, spell_id):
        mana_spell_rating = 0
        if spell_id == 12051:
            if self.char.current_mana / self.char.total_mana <= 0.35:
                mana_spell_rating += 1
            else:
                mana_spell_rating += -1
        else:
            mana_spell_rating += 1
        return mana_spell_rating

    def get_consumable_rating(self, item_id):
        consumable_rating = 0
        item_info = DB.get_item(item_id)
        for i in range(1, 6):
            item_spell = DB.get_spell(item_info[DB.item_column_info["spellid_" + str(i)]])
            if item_spell:
                if item_id in (5513, 5514, 8007, 8008, 22044, 22832):
                    for effect_slot in range(1, 4):
                        max_value = item_spell[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                                    item_spell[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
                                    item_spell[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
                        if max_value != 0 and max_value < (self.char.total_mana - self.char.current_mana):
                            consumable_rating += 1 + \
                                                 (self.char.total_mana - self.char.current_mana) / self.char.total_mana
                elif item_id in (22839,):
                    if self.char.current_mana / self.char.total_mana > 0.35:
                        consumable_rating += 0.4 + self.char.current_mana / self.char.total_mana

        return consumable_rating

    def get_boost_spell_rating(self, spell_id):
        spell_info = DB.get_spell(spell_id)
        spell_rating = self.get_boost_spell_base_rating()
        # TODO consider spell specific conditions

        return spell_rating

    def get_boost_spell_base_rating(self):
        spell_rating = -1
        spell_rating += (self.char.current_mana / self.char.total_mana) + 0.7

        if self.env.now / self.results.sim_length > 0.65:
            spell_rating += self.env.now / self.results.sim_length

        return spell_rating

    def get_offensive_spell_rating(self, spell_id):
        spell_info = DB.get_spell(spell_id)

        spell_damage = 0
        for i in range(1, 4):
            # TODO consider other effects
            if spell_info[DB.spell_column_info["Effect" + str(i)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] in [6, 77]:
                spell_damage += self.get_direct_spell_damage(i, spell_id, spell_info)

            elif spell_info[DB.spell_column_info["Effect" + str(i)]] == 6 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] in [6, 25] and \
                    spell_info[DB.spell_column_info["EffectApplyAuraName" + str(i)]] == 3:
                spell_base_damage = self.get_avg_effect_strength(spell_info, i)
                spell_base_damage = spell_base_damage * \
                                    enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]] / \
                                    spell_info[DB.spell_column_info["EffectAmplitude" + str(i)]]

                spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                          * self.char.spell_handler.enemy_damage_taken_mod(spell_info[0])

                spell_damage += round(spell_base_damage *
                                      spell_damage_multiplier)
            elif spell_info[DB.spell_column_info["Effect" + str(i)]] == 6 and \
                    spell_info[DB.spell_column_info["EffectApplyAuraName" + str(i)]] in [23]:

                triggered_spell_id = spell_info[DB.spell_column_info["EffectTriggerSpell" + str(i)]]
                triggered_spell_info = DB.get_spell(triggered_spell_id)
                triggered_spell_total_damage = 0

                for triggered_spell_slot in range(1, 4):
                    if triggered_spell_info[DB.spell_column_info["Effect" + str(triggered_spell_slot)]] == 2 and \
                            triggered_spell_info[
                                DB.spell_column_info["EffectImplicitTargetA" + str(triggered_spell_slot)]] in [6, 77]:
                        triggered_spell_total_damage += self.get_direct_spell_damage(triggered_spell_slot,
                                                                                     triggered_spell_id,
                                                                                     triggered_spell_info)

                channel_duration, channel_interval = self.char.spell_handler.periodic_effect_behaviour(spell_info, i)
                triggered_spell_total_damage *= channel_duration / channel_interval + 1

                spell_damage += triggered_spell_total_damage

        spell_damage = spell_damage * spell_damage * 0.7

        spell_mana_cost = self.char.spell_resource_cost(spell_id, proc_auras=False)
        spell_mana_cost = spell_mana_cost if spell_mana_cost != 0 else 1

        if spell_info[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_info[DB.spell_column_info["AttributesEx"]] & 64:
            spell_time = enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]]
        else:
            spell_time = self.char.spell_cast_time(spell_id, proc_auras=False)

        normalized_spell_time = max(spell_time, 1500)

        spell_rating = spell_damage / normalized_spell_time / spell_mana_cost - 1

        # print(DB.get_spell_name(spell_id) + str(spell_id), spell_rating)

        return spell_rating

    def get_direct_spell_damage(self, i, spell_id, spell_info):
        spell_base_damage = self.get_avg_effect_strength(spell_info, i)
        spell_spell_power = self.char.spell_spell_power(spell_id)
        spell_power_coefficient = self.char.spell_power_coefficient(spell_id, proc_auras=False)
        spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                  * self.char.spell_handler.enemy_damage_taken_mod(spell_info[0])
        spell_crit_damage_multiplier = self.char.spell_crit_dmg_multiplier(spell_id, proc_auras=False)
        spell_crit_chance_spell = self.char.spell_crit_chance_spell(spell_id, proc_auras=False)

        # non crit damage
        spell_damage = (spell_base_damage + spell_spell_power * spell_power_coefficient) * spell_damage_multiplier
        # return non crit damage + avg per spell crit damage
        return round(spell_damage + spell_damage * spell_crit_damage_multiplier * spell_crit_chance_spell / 100)

    @lru_cache
    def get_avg_effect_strength(self, spell_info, effect_slot):
        min_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * 1
        max_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
                    spell_info[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
        return round((min_value + max_value) / 2)

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

        self.env.process(self.five_second_rule())
        self.five_second_rule()
        if not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 4 and \
                not DB.get_spell(spell_id)[DB.spell_column_info["AttributesEx"]] & 64:
            self.results.spell_cast(spell_id, self.env.now)

        self.char.cast_mana_spell(spell_id)
        self.char.spell_handler.spell_start_cooldown(spell_id)
        self.char.spell_handler.apply_spell_effect(spell_id)
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
                # delete some active items after charges used eg. mana gems
                if item_info[DB.item_column_info["spellcharges_" + str(i)]]\
                        + self.char.active_consumables[item_id] == 0 \
                        and item_info[DB.item_column_info["spellcategory_" + str(i)]] == 1153:
                    del self.char.active_consumables[item_id]
