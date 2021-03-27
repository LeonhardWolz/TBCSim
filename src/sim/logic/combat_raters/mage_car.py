from src import enums
from src.sim.logic.combat_raters.combat_action_rater import CombatActionRater

import src.db.db_connector as DB


class MageCAR(CombatActionRater):

    def get_mana_spell_rating(self, spell_id):
        mana_spell_rating = 0
        if spell_id == 12051:
            if self.player.char.current_mana / self.player.char.total_mana <= 0.35:
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
                                    (item_spell[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] *
                                     item_spell[DB.spell_column_info["EffectDieSides" + str(effect_slot)]])
                        if max_value != 0:
                            consumable_rating += -0.8 + max_value / self.player.char.total_mana + \
                                                 (self.player.char.total_mana - self.player.char.current_mana) \
                                                 / self.player.char.total_mana
                elif item_id in (22839,):
                    if self.player.char.current_mana / self.player.char.total_mana > 0.35:
                        consumable_rating += -0.5 + self.player.char.current_mana / self.player.char.total_mana

        return consumable_rating

    def get_boost_spell_rating(self, spell_id):
        spell_rating = self.get_boost_spell_base_rating()

        return spell_rating

    def get_offensive_spell_rating(self, spell_id):
        spell_info = DB.get_spell(spell_id)

        spell_effect_weight = 0
        for i in range(1, 4):
            # TODO consider other effects
            # Direct spell damage
            if spell_info[DB.spell_column_info["Effect" + str(i)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] in [6, 77]:
                spell_effect_weight += self.get_direct_spell_damage(i, spell_id, spell_info)

            # Dot spell damage
            elif spell_info[DB.spell_column_info["Effect" + str(i)]] == 6 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(i)]] in [6, 25] and \
                    spell_info[DB.spell_column_info["EffectApplyAuraName" + str(i)]] == 3:
                spell_effect_weight += self.get_dot_spell_damage(i, spell_id, spell_info)

            # Channelled spell triggered spell damage
            elif spell_info[DB.spell_column_info["Effect" + str(i)]] == 6 and \
                    spell_info[DB.spell_column_info["EffectApplyAuraName" + str(i)]] in [23]:
                spell_effect_weight += self.get_channelled_spell_damage(i, spell_info)

        spell_effect_weight = spell_effect_weight * spell_effect_weight * 0.7

        spell_mana_cost = self.player.char.spell_resource_cost(spell_id, proc_auras=False)
        spell_mana_cost = spell_mana_cost if spell_mana_cost != 0 else 1

        if spell_info[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_info[DB.spell_column_info["AttributesEx"]] & 64:
            spell_time = enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]]
        else:
            spell_time = self.player.char.spell_cast_time(spell_id, proc_auras=False)

        normalized_spell_time = max(spell_time, 1500)

        spell_rating = spell_effect_weight / (normalized_spell_time * 1.2) / (spell_mana_cost * 0.7) - 1

        #self.player.logg(str(DB.get_spell_name(spell_id)) + str(spell_id) + ": " + str(spell_rating))

        return spell_rating
