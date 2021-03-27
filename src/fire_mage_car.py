from src import enums
from src.mage_car import MageCAR

import src.db_connector as DB


class FireMageCAR(MageCAR):
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

        spell_rating = -1 + (spell_effect_weight * 2.2 / normalized_spell_time) - spell_mana_cost * 0.0002 + spell_effect_weight / (spell_mana_cost * 20)

        #scorch rating modification
        if spell_info[DB.spell_column_info["SpellFamilyFlags"]] & 16:
            aura = [aura for aura in self.player.char.spell_handler.enemy.active_auras if aura.spell_id == 22959]
            stacks = aura[0].curr_stacks if aura else 0
            if stacks != 5 or aura and\
                    (aura[0].create_time + enums.duration_index[aura[0].duration_index] - 10000) < self.player.env.now:
                spell_rating *= 1.3
            else:
                spell_rating *= 0.9

        self.player.logg(str(DB.get_spell_name(spell_id)) + str(spell_id) + ": " + str(spell_rating) + ": " + str(spell_effect_weight) + ": " + str(spell_time) + ": " + str(normalized_spell_time))

        return spell_rating
