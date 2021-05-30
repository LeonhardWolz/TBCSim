from src import enums
from src.enums import CombatAction
import src.db.sqlite_db_connector as DB


class CombatActionRater(object):

    def __init__(self, player):
        self.player = player

    def get_next_combat_action(self):
        misc_combat_action = self.get_misc_combat_action()
        if misc_combat_action is not None:
            return misc_combat_action

        damage_spell_action = self.get_damage_spell_action()
        if damage_spell_action is not None:
            return damage_spell_action

        if self.player.char.has_wand_range_attack():
            return [CombatAction.Wand_Attack]

        return [CombatAction.Idle]

    def get_misc_combat_action(self):
        misc_combat_actions_to_consider = []
        for spell_id in self.player.char.mana_spells:
            if not self.player.char.combat_handler.spell_on_cooldown(spell_id):
                misc_combat_actions_to_consider.append({"combat_action": [CombatAction.Cast_Spell, spell_id],
                                                        "combat_rating": self.get_mana_spell_rating(spell_id)})

        for item_id in self.player.char.active_consumables.keys():
            if not self.player.char.combat_handler.item_on_cooldown(item_id):
                misc_combat_actions_to_consider.append({"combat_action": [CombatAction.Consume_Item, item_id],
                                                        "combat_rating": self.get_item_rating(item_id)})
        for spell_id in self.player.char.boost_spells:
            if not self.player.char.combat_handler.spell_on_cooldown(spell_id) and \
                    self.player.char.has_mana_to_cast_spell(spell_id):
                misc_combat_actions_to_consider.append({"combat_action": [CombatAction.Cast_Spell, spell_id],
                                                        "combat_rating": self.get_boost_spell_rating(spell_id)})

        misc_combat_actions_to_consider.sort(key=lambda x: x["combat_rating"])

        #print(self.player.env.now, [(x["combat_action"], x["combat_rating"]) for x in misc_combat_actions_to_consider])

        if misc_combat_actions_to_consider:
            misc_combat_action = misc_combat_actions_to_consider.pop()
            if misc_combat_action["combat_rating"] > 0:
                return misc_combat_action["combat_action"]

        return None

    def get_damage_spell_action(self):
        damage_spells_to_consider = []
        for spell_id in self.player.char.damage_spells:
            if not self.player.char.combat_handler.spell_on_cooldown(spell_id) \
                    and self.player.char.has_mana_to_cast_spell(spell_id):
                damage_spells_to_consider.append({"spell_id": spell_id,
                                                  "spell_rating": self.get_offensive_spell_rating(spell_id)})

        damage_spells_to_consider.sort(key=lambda x: x["spell_rating"])

        #print(self.player.env.now, [(x["spell_id"], x["spell_rating"]) for x in damage_spells_to_consider])

        if damage_spells_to_consider:
            spell_to_consider = damage_spells_to_consider.pop()

            if spell_to_consider["spell_rating"] > 0:
                return [CombatAction.Cast_Spell, spell_to_consider["spell_id"]]
            else:
                return None
        else:
            return None

    def get_mana_spell_rating(self, spell_id):
        raise NotImplementedError

    def get_item_rating(self, item_id):
        raise NotImplementedError

    def get_boost_spell_rating(self, spell_id):
        raise NotImplementedError

    def get_boost_base_rating(self):
        spell_rating = -0.6
        spell_rating += (self.player.char.current_mana / self.player.char.total_mana)

        if self.player.env.now / self.player.results.sim_length > 0.65:
            spell_rating += self.player.env.now / self.player.results.sim_length

        return spell_rating

    def get_offensive_spell_rating(self, spell_id):
        raise NotImplementedError

    def get_direct_spell_damage(self, effect_slot, spell_id, spell_info):
        """Calculates avg direct spell damage, including critical hits and any triggered effects"""
        mindamage, maxdamage = self.player.char.combat_handler.get_effect_strength(spell_info, effect_slot)
        spell_base_damage = round(mindamage + maxdamage / 2)

        spell_spell_power = self.player.char.spell_spell_power(spell_id)
        spell_power_coefficient = self.player.char.spell_power_coefficient(spell_id, proc_auras=False)
        spell_damage_multiplier = self.player.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                  * self.player.char.combat_handler.enemy_damage_taken_mod(spell_id)
        spell_crit_damage_multiplier = self.player.char.spell_crit_dmg_multiplier(spell_id, proc_auras=False)
        spell_crit_chance_spell = self.player.char.spell_crit_chance_spell(spell_id, proc_auras=False)

        # non crit damage
        spell_damage = (spell_base_damage + spell_spell_power * spell_power_coefficient) * spell_damage_multiplier

        # non crit damage + per spell avg crit damage
        spell_crit_damage = spell_damage * spell_crit_damage_multiplier * (spell_crit_chance_spell / 100)

        # print(spell_id, round(spell_damage), round(spell_crit_damage), spell_crit_damage_multiplier, spell_crit_chance_spell)

        # add avg ignite dmg
        if DB.get_spell_school(spell_id) & 4:
            for aura in [aura for aura in self.player.char.combat_handler.active_auras if
                         aura.spell_id in [11119, 11120, 12846, 12847, 12848]]:
                spell_crit_damage += spell_crit_damage * (enums.ignite_dmg_pct[aura.spell_id] / 100)
        return spell_damage + spell_crit_damage

    def get_dot_spell_damage(self, effect_slot, spell_id, spell_info):
        mindamage, maxdamage = self.player.char.combat_handler.get_effect_strength(spell_info, effect_slot)
        spell_base_damage = round(mindamage + maxdamage / 2)
        spell_base_damage = spell_base_damage * \
                            enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]] / \
                            spell_info[DB.spell_column_info["EffectAmplitude" + str(effect_slot)]]
        spell_damage_multiplier = self.player.char.spell_dmg_multiplier(spell_id, proc_auras=False) \
                                  * self.player.char.combat_handler.enemy_damage_taken_mod(spell_info[0])

        return round(spell_base_damage * spell_damage_multiplier)

    def get_channelled_spell_damage(self, effect_slot, spell_info):
        triggered_spell_id = spell_info[DB.spell_column_info["EffectTriggerSpell" + str(effect_slot)]]
        triggered_spell_info = DB.get_spell(triggered_spell_id)
        triggered_spell_total_damage = 0
        for triggered_spell_slot in range(1, 4):
            if triggered_spell_info[DB.spell_column_info["Effect" + str(triggered_spell_slot)]] == 2 and \
                    triggered_spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(triggered_spell_slot)]] \
                    in [6, 77]:
                triggered_spell_total_damage += self.get_direct_spell_damage(triggered_spell_slot,
                                                                             triggered_spell_id,
                                                                             triggered_spell_info)
        channel_duration, channel_interval = self.player.char.combat_handler.periodic_effect_behaviour(spell_info,
                                                                                                       effect_slot)

        return triggered_spell_total_damage * channel_duration / channel_interval + 1

    # @lru_cache
    # def get_avg_effect_strength(self, spell_info, effect_slot):
    #     min_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
    #                 spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * 1
    #     max_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
    #                 spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
    #                 spell_info[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
    #     return round((min_value + max_value) / 2)
