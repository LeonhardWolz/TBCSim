from src import enums
from src.sim.logic.combat_raters.mage_car import MageCAR

import src.db.sqlite_db_connector as DB


class FireMageCAR(MageCAR):
    def get_item_rating(self, item_id):
        consumable_rating = 0
        item_info = DB.get_item(item_id)
        for i in range(1, 6):
            item_spell = DB.get_spell(item_info[DB.item_column_info["spellid_" + str(i)]])
            if item_spell and item_info[DB.item_column_info["spelltrigger_" + str(i)]] == 0:
                # mana restoration items
                if item_id in (5513, 5514, 8007, 8008, 22044, 22832):
                    for effect_slot in range(1, 4):
                        max_value = item_spell[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                                    (item_spell[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] *
                                     item_spell[DB.spell_column_info["EffectDieSides" + str(effect_slot)]])
                        if max_value != 0:
                            consumable_rating += -0.8 + max_value / self.player.char.total_mana + \
                                                 (self.player.char.total_mana - self.player.char.current_mana) \
                                                 / self.player.char.total_mana
                # damage boost items
                else:
                    consumable_rating += self.get_boost_base_rating()

        return consumable_rating

    def get_boost_spell_rating(self, spell_id):
        return self.get_boost_base_rating()

    def get_boost_base_rating(self):
        return super().get_boost_base_rating() + self.scorch_modifier()

    def scorch_modifier(self):
        aura = [aura for aura in self.player.char.combat_handler.enemy.active_auras if aura.spell_id == 22959]
        if not aura or aura[0].curr_stacks != 5:
            return -0.6 - 0.1 * (0 if not aura else 5 - aura[0].curr_stacks)
        else:
            return 0.3

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

        spell_mana_cost = self.player.char.spell_resource_cost(spell_id, proc_auras=False)
        spell_mana_cost = spell_mana_cost if spell_mana_cost != 0 else 1

        if spell_info[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_info[DB.spell_column_info["AttributesEx"]] & 64:
            spell_time = enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]]
        else:
            spell_time = self.player.char.spell_cast_time(spell_id, proc_auras=False)

        normalized_spell_time = max(spell_time, 1500)
        spell_rating = -1 + (spell_effect_weight * 2 / normalized_spell_time) \
                       - spell_mana_cost * 0.002 \
                       + spell_effect_weight / (spell_mana_cost * 20)

        # scorch rating modification
        if spell_info[DB.spell_column_info["SpellFamilyFlags"]] & 16:
            aura = [aura for aura in self.player.char.combat_handler.enemy.active_auras if aura.spell_id == 22959]

            if not aura or aura[0].curr_stacks != 5:
                # Apply 5 stacks of improved scorch
                spell_rating *= 0.9 + (self.player.char.current_mana / self.player.char.total_mana) * 0.4
            elif aura[0].create_time + enums.duration_index[aura[0].duration_index] - 10000 < self.player.env.now:
                # Refresh of improved scorch more urgent the closer it is to running out
                mod = (self.player.env.now -
                       (aura[0].create_time + enums.duration_index[aura[0].duration_index] - 10000)) \
                      / 10000
                spell_rating *= 1 + mod * 0.4
            else:
                # Small penalty if improved scorch already applied
                spell_rating *= 0.9

        return spell_rating
