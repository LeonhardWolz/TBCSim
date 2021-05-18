import random
from functools import lru_cache

from src import enums
from src.sim.exceptions.exceptions import NotImplementedWarning
from src.sim.sim_objects.aura import Aura
from src.sim.sim_objects.channelled_spell import ChannelledSpell
from src.sim.sim_objects.dot_spell import DotSpell
import src.db.sqlite_db_connector as DB


class SpellHandler:

    def __init__(self, char):
        self.char = char
        self.active_auras = []
        self.enemy = None
        self.env = None
        self.results = None
        self.sim_num = None

        self.cooldown_spell_id = {}
        self.cooldown_spell_family_mask = {}
        self.cooldown_item_id = {}
        self.cooldown_item_family_mask = {}

    def apply_spell_effect_delay(self, spell_id):
        spell_info = DB.get_spell(spell_id)
        speed = spell_info[DB.spell_column_info["Speed"]]
        if speed != 0:
            yield self.env.timeout(int(self.enemy.distance / speed * 1000))
        #
        # # 100ms Delay to imitate reaction time and lag
        # yield self.env.timeout(100)
        self.apply_spell_effect(spell_id)

    def apply_spell_effect(self, spell_id, item_id=0):
        spell_info = DB.get_spell(spell_id)

        for j in range(1, 4):
            if spell_info[DB.spell_column_info["Effect" + str(j)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] in [6, 77]:
                # Deal spell school damage to enemy
                self.process_direct_damage_spell(spell_info, j)

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 1:

                # Deal spell school damage to character
                raise NotImplementedWarning("Damage to character not implemented")

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 4 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 1:

                # Apply Dummy Aura to character
                self.apply_aura_to_character(spell_info, j)

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 6:

                # Dont apply fire power + piercing ice aura with item type mask
                if spell_info[DB.spell_column_info["EffectItemType" + str(j)]] == 0 or \
                        spell_id not in [11124, 12378, 12398, 12399, 12400, 11151, 12952, 12953, 12954, 12957]:
                    self.apply_passive_auras(spell_info, j)

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 64 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 1:

                # Trigger Spell on character
                self.apply_spell_effect(spell_info[DB.spell_column_info["EffectTriggerSpell" + str(j)]])

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 3 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 1:
                # berserking
                if spell_id == 20554:
                    self.berserking()

                # cold snap
                if spell_id == 11958:
                    self.cold_snap(spell_id)
            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 30:

                self.energize(spell_info, j, item_id)
            elif spell_info[DB.spell_column_info["Effect" + str(j)]] != 0:
                raise NotImplementedWarning("Effect " + str(j) + " of Spell could not be handled: " + str(spell_info))

    def apply_passive_auras(self, spell_info, effect_slot):
        if (spell_info[DB.spell_column_info["AttributesEx"]] & 4 or
            spell_info[DB.spell_column_info["AttributesEx"]] & 64) and \
                spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]] in [21, 23]:
            self.process_channelled_spell(spell_info, effect_slot)

        elif spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(effect_slot)]] in [1, 21]:
            self.apply_aura_to_character(spell_info, effect_slot)

        elif spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(effect_slot)]] in [6, 25]:
            if spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]] == 3:
                # Apply periodic damage
                self.process_dot_damage_spell(spell_info, effect_slot)
            else:
                self.apply_aura_to_enemy(spell_info, effect_slot)

    def apply_aura_to_character(self, spell_info, effect_slot):
        modified_aura = False
        for aura in self.active_auras:
            if aura.spell_id == spell_info[0] and \
                    aura.aura_id == spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]] and \
                    aura.misc_value == spell_info[DB.spell_column_info["EffectMiscValue" + str(effect_slot)]]:
                if aura.stack_limit is not aura.curr_stacks:
                    aura.curr_stacks += 1
                aura.create_time = self.env.now if self.env else 0
                modified_aura = True

        if not modified_aura:
            self.active_auras.append(self.get_aura(spell_info, effect_slot))

    def apply_aura_to_enemy(self, spell_info, effect_slot):
        modified_aura = False
        for aura in self.enemy.active_auras:
            if aura.spell_id == spell_info[0] and \
                    aura.aura_id == spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]] and \
                    aura.misc_value == spell_info[DB.spell_column_info["EffectMiscValue" + str(effect_slot)]]:
                if aura.stack_limit is not aura.curr_stacks:
                    aura.curr_stacks += 1
                aura.create_time = self.env.now
                modified_aura = True

        if not modified_aura:
            self.enemy.active_auras.append(self.get_aura(spell_info, effect_slot))

            # Check and roll to apply frostbite if spell applies chill
            if spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]] == 33:
                for aura in self.char.spell_handler.active_auras:
                    if aura.spell_id in [11071, 12496, 12497] and aura.value > random.randint(0, 100):
                        self.apply_spell_effect(aura.trigger_spell)

    def get_aura(self, spell_info, effect_slot):
        minvalue, maxvalue = self.get_effect_strength(spell_info, effect_slot)
        value = random.randint(minvalue, maxvalue)
        aura_id = spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]]
        misc_value = spell_info[DB.spell_column_info["EffectMiscValue" + str(effect_slot)]]

        # Increase clearcasting crit chance from Arcane Potency
        if spell_info[0] == 12536 and aura_id == 57:
            for aura in [aura for aura in self.active_auras if aura.spell_id in [31571, 31572, 31573]]:
                value += aura.value

        affected_spell_school = spell_info[DB.spell_column_info["SchoolMask"]]
        affected_spell_family_info = DB.get_spell_family_affected(spell_info[0])
        affected_spell_family_info.sort(key=lambda x: x[1])
        if affected_spell_family_info is not None and len(affected_spell_family_info) >= effect_slot and \
                affected_spell_family_info[(effect_slot - 1)][1] == (effect_slot - 1):
            affected_spell_family_mask = affected_spell_family_info[(effect_slot - 1)][2]
        else:
            affected_spell_family_mask = 0

        affected_item_class = spell_info[DB.spell_column_info["EquippedItemClass"]]
        affected_item_subclass_mask = spell_info[DB.spell_column_info["EquippedItemSubClassMask"]]

        if self.env is None:
            create_time = 0
        else:
            create_time = self.env.now

        duration_index = spell_info[DB.spell_column_info["DurationIndex"]]
        stack_limit = spell_info[DB.spell_column_info["StackAmount"]]
        trigger_spell = spell_info[DB.spell_column_info["EffectTriggerSpell" + str(effect_slot)]]
        proc = [spell_info[DB.spell_column_info["ProcFlags"]],
                spell_info[DB.spell_column_info["ProcChance"]],
                spell_info[DB.spell_column_info["ProcCharges"]]]
        attributes = [spell_info[DB.spell_column_info["Attributes"]],
                      spell_info[DB.spell_column_info["AttributesEx"]],
                      spell_info[DB.spell_column_info["AttributesEx2"]],
                      spell_info[DB.spell_column_info["AttributesEx3"]],
                      spell_info[DB.spell_column_info["AttributesEx4"]],
                      spell_info[DB.spell_column_info["AttributesEx5"]],
                      spell_info[DB.spell_column_info["AttributesEx6"]]]

        return Aura(value=value,
                    spell_id=spell_info[0],
                    aura_id=aura_id,
                    misc_value=misc_value,
                    stack_limit=stack_limit,
                    affected_spell_school=affected_spell_school,
                    affected_spell_family_mask=affected_spell_family_mask,
                    affected_item_class=affected_item_class,
                    affected_item_subclass_mask=affected_item_subclass_mask,
                    create_time=create_time,
                    duration_index=duration_index,
                    trigger_spell=trigger_spell,
                    proc=proc,
                    attributes=attributes)

    @staticmethod
    @lru_cache(maxsize=None, typed=False)
    def get_effect_strength(spell_info, effect_slot):
        level_effect_strength = spell_info[DB.spell_column_info["EffectRealPointsPerLevel" + str(effect_slot)]] * \
                                (spell_info[DB.spell_column_info["MaxLevel"]] -
                                 spell_info[DB.spell_column_info["BaseLevel"]])

        min_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * 1
        max_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
                    spell_info[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
        return round(min_value + level_effect_strength), round(max_value + level_effect_strength)

    @staticmethod
    def periodic_effect_behaviour(spell_info, effect_slot):
        return enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]], \
               spell_info[DB.spell_column_info["EffectAmplitude" + str(effect_slot)]]

    @staticmethod
    def spell_flat_mana_cost(spell_id):
        return DB.get_spell(spell_id)[DB.spell_column_info["ManaCost"]]

    @staticmethod
    def spell_pct_mana_cost(spell_id):
        return DB.get_spell(spell_id)[DB.spell_column_info["ManaCostPercentage"]]

    @staticmethod
    def spell_cast_time(spell_id):
        return enums.cast_time[
            DB.get_spell(spell_id)[DB.spell_column_info["CastingTimeIndex"]]]

    @staticmethod
    def spell_power_coefficient(spell_id, effect_slot=4):
        spell_from_db = DB.get_spell(spell_id)

        def spell_aoe_divisor():
            for x in [22, 24, 28 - 31, 33, 34]:
                if x in [spell_from_db[DB.spell_column_info["EffectImplicitTargetA" + str(1)]],
                         spell_from_db[DB.spell_column_info["EffectImplicitTargetA" + str(2)]],
                         spell_from_db[DB.spell_column_info["EffectImplicitTargetA" + str(3)]]]:
                    return 2
            return 1

        def spell_slow_multiplier():
            if 33 in [spell_from_db[DB.spell_column_info["EffectApplyAuraName" + str(1)]],
                      spell_from_db[DB.spell_column_info["EffectApplyAuraName" + str(2)]],
                      spell_from_db[DB.spell_column_info["EffectApplyAuraName" + str(3)]]]:
                return 0.95
            return 1

        def spell_downrank_penalty():
            spell_level = spell_from_db[DB.spell_column_info["SpellLevel"]]
            if spell_level < 20:
                return 1 - (20 - spell_level) * 0.0375
            return 1

        # Pyroblast dot 70%
        if spell_from_db[DB.spell_column_info["SchoolMask"]] & 4194304 and \
                spell_from_db[DB.spell_column_info["Effect" + str(effect_slot)]] == 6:
            return 0.7

        # channeled spell
        if spell_from_db[DB.spell_column_info["AttributesEx"]] & 4 or \
                spell_from_db[DB.spell_column_info["AttributesEx"]] & 64:
            base_cast_time = enums.duration_index[spell_from_db[DB.spell_column_info["DurationIndex"]]]

        # cast spell
        else:
            base_cast_time = enums.cast_time[spell_from_db[DB.spell_column_info["CastingTimeIndex"]]]

        # arcane missiles special case
        if spell_from_db[DB.spell_column_info["SpellFamilyFlags"]] & 2097152:
            return round(1 / spell_aoe_divisor() * spell_slow_multiplier() * spell_downrank_penalty() / 5, 3)

        # Instant Spells are counted as 1.5s casts. casts longer than 3.5s are considered 3.5s casts
        return round(min(max(base_cast_time, 1500), 3500)
                     / 3500
                     / spell_aoe_divisor()
                     * spell_slow_multiplier()
                     * spell_downrank_penalty(), 3)

    def spell_does_hit(self, spell_id=0):
        # TODO consider player and enemy level. currently player=70 enemy=73 boss
        return random.uniform(0.00, 100.00) < (83 + self.char.spell_hit_chance_spell(spell_id))

    def spell_does_crit(self, spell_id=0):
        return random.uniform(0.00, 100.00) < self.char.spell_crit_chance_spell(spell_id)

    def process_direct_damage_spell(self, spell_info, effect_slot):
        self.on_impact(spell_info)
        if self.spell_does_hit(spell_info[0]):
            minvalue, maxvalue = self.get_effect_strength(spell_info, effect_slot)
            spell_base_damage = random.randint(minvalue, maxvalue)
            spell_spell_power = self.char.spell_spell_power(spell_info[0])
            spell_power_coefficient = self.char.spell_power_coefficient(spell_info[0])
            spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_info[0]) \
                                      * self.enemy_damage_taken_mod(spell_info[0])

            spell_damage = round((spell_base_damage + spell_spell_power * spell_power_coefficient)
                                 * spell_damage_multiplier)

            if self.spell_does_crit(spell_info[0]):
                spell_damage *= self.char.spell_crit_dmg_multiplier(spell_info[0])
                spell_damage = round(spell_damage)

                self.on_spell_crit(spell_info[0], spell_damage)
                self.logg(spell_info[DB.spell_column_info["SpellName"]] + " " +
                          (spell_info[DB.spell_column_info["Rank1"]] or "") + " critical damage: " +
                          str(spell_damage))
                self.results.damage_spell_crit(spell_info[0],
                                               spell_info[DB.spell_column_info["SpellName"]] + " " +
                                               (spell_info[DB.spell_column_info["Rank1"]] or ""),
                                               spell_damage)
            else:
                self.on_spell_hit(spell_info[0])
                self.logg(spell_info[DB.spell_column_info["SpellName"]] + " " +
                          (spell_info[DB.spell_column_info["Rank1"]] or "") + " damage: " +
                          str(spell_damage))
                self.results.damage_spell_hit(spell_info[0],
                                              spell_info[DB.spell_column_info["SpellName"]] + " " +
                                              (spell_info[DB.spell_column_info["Rank1"]] or ""),
                                              spell_damage)
        else:
            self.logg(spell_info[DB.spell_column_info["SpellName"]] + " " +
                      (spell_info[DB.spell_column_info["Rank1"]] or "") + " resisted")
            self.results.damage_spell_resisted(spell_info[0],
                                               spell_info[DB.spell_column_info["SpellName"]] + " " +
                                               (spell_info[DB.spell_column_info["Rank1"]] or ""))

    def process_dot_damage_spell(self, spell_info, effect_slot):
        # TODO Consider all Character Stats for damage
        if self.spell_does_hit(spell_info[0]):
            dot_duration, dot_interval = self.periodic_effect_behaviour(spell_info, effect_slot)
            spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_info[0]) \
                                      * self.enemy_damage_taken_mod(spell_info[0])

            minvalue, maxvalue = self.get_effect_strength(spell_info, effect_slot)
            spell_base_damage = random.randint(minvalue, maxvalue)
            dot_damage = round(spell_base_damage * spell_damage_multiplier)

            self.env.process(DotSpell(self.env,
                                      self,
                                      spell_info[0],
                                      dot_damage,
                                      dot_interval,
                                      dot_duration,
                                      self.results).ticking())
        else:
            self.logg(spell_info[DB.spell_column_info["SpellName"]] + " " +
                      (spell_info[DB.spell_column_info["Rank1"]] or "") + " dot resisted")
            self.results.dot_spell_resisted(spell_info[0],
                                            spell_info[DB.spell_column_info["SpellName"]] + " " +
                                            (spell_info[DB.spell_column_info["Rank1"]] or ""))

    def process_channelled_spell(self, spell_info, effect_slot):
        aura_id = spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]]

        channel_duration, channel_interval = self.periodic_effect_behaviour(spell_info, effect_slot)
        channelled_spell = ChannelledSpell(
            spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]],
            self.env,
            self,
            spell_info[0],
            channel_interval,
            channel_duration,
            self.results)

        if aura_id == 21:
            self.results.spell_cast(spell_info[0],
                                    spell_info[DB.spell_column_info["SpellName"]] + " " +
                                    (spell_info[DB.spell_column_info["Rank1"]] or ""),
                                    self.env.now)
            minvalue, maxvalue = self.get_effect_strength(spell_info, effect_slot)
            channelled_spell.value = random.randint(minvalue, maxvalue)

        elif aura_id == 23:
            trigger_spell_id = spell_info[DB.spell_column_info["EffectTriggerSpell" + str(effect_slot)]]
            self.results.spell_cast(trigger_spell_id,
                                    DB.get_spell_name(trigger_spell_id) + " " +
                                    (DB.get_spell(trigger_spell_id)[DB.spell_column_info["Rank1"]] or ""),
                                    self.env.now)
            channelled_spell.trigger_spell = trigger_spell_id

        self.env.process(channelled_spell.channel())

    def process_wand_attack(self):
        if self.spell_does_hit():
            min_wand_damage, max_wand_damage = self.char.get_weapon_damage(18)
            wand_damage = random.randint(min_wand_damage, max_wand_damage)
            if self.spell_does_crit():
                wand_damage = round(wand_damage * 1.5)
                self.logg(self.char.gear[18].name + " wand attack critical damage: " + str(wand_damage))
                self.results.wand_attack_crit(self.char.gear[18].item_data[0],
                                              self.char.gear[18].item_data[DB.item_column_info["name"]],
                                              wand_damage)
            else:
                self.logg(self.char.gear[18].name + " wand attack damage: " + str(wand_damage))
                self.results.wand_attack_hit(self.char.gear[18].item_data[0],
                                             self.char.gear[18].item_data[DB.item_column_info["name"]],
                                             wand_damage)

        else:
            self.logg(self.char.gear[18].name + " wand attack resisted")
            self.results.wand_attack_resisted(self.char.gear[18].item_data[0],
                                              self.char.gear[18].item_data[DB.item_column_info["name"]])

    def energize(self, spell_info, effect_slot, item_id=0):
        minvalue, maxvalue = self.get_effect_strength(spell_info, effect_slot)
        mana_restored = random.randint(minvalue, maxvalue)
        self.logg("Restored " + str(mana_restored) + " Mana")
        if item_id != 0:
            self.results.item_mana_restored(item_id, mana_restored)
        self.char.current_mana += mana_restored

    def enemy_damage_taken_mod(self, spell_id):
        dmg_taken_mod = 1
        # for aura in self.get_enemy_mod_auras(spell_id):
        for aura in self.enemy.active_auras:
            if aura.aura_id == 87 and \
                    aura.affected_spell_school & DB.get_spell(spell_id)[DB.spell_column_info["SchoolMask"]]:
                dmg_taken_mod *= 1 + (aura.value * aura.curr_stacks / 100)

        return dmg_taken_mod

    def curr_sim_time_str(self):
        return str(self.env.now / 1000)

    def remove_expired_auras(self):
        for aura in self.active_auras:
            if aura.duration_index != 0 and \
                    self.env.now - aura.create_time > enums.duration_index[aura.duration_index] != -1:
                self.active_auras.remove(aura)
        for aura in self.enemy.active_auras:
            if aura.duration_index != 0 and \
                    self.env.now - aura.create_time > enums.duration_index[aura.duration_index] != -1:
                self.enemy.active_auras.remove(aura)

    def proc_aura_charge(self, aura):
        aura.procced()
        if aura.proc[2] - aura.proc_counter == 0:
            # Handle Combustion Auras
            if aura.spell_id == 11129:
                self.remove_auras_from_spell(28682)
                self.spell_start_cooldown(aura.spell_id)
            self.active_auras.remove(aura)

    def remove_auras_from_spell(self, spell_id):
        for aura in self.active_auras[:]:
            if aura.spell_id == spell_id:
                self.active_auras.remove(aura)

    def logg(self, info):
        self.results.logg("{:8s} {}".format(self.curr_sim_time_str(), info))

    def on_impact(self, spell_info):
        # Mage
        if spell_info[DB.spell_column_info["SpellFamilyName"]] == 3:
            # Arcane Blast
            if spell_info[DB.spell_column_info["SpellFamilyFlags"]] & 0x20000000:
                self.apply_spell_effect(36032)

    @lru_cache
    def get_spell_gcd(self, spell_id):
        return DB.get_spell_gcd(spell_id)

    def aura_applies_to_spell(self, aura, spell_id):
        if aura.affected_spell_family_mask & DB.get_spell_family(spell_id) != 0 or \
                (self.spell_has_triggered_spell(spell_id) and aura.affected_spell_family_mask &
                 DB.get_spell_family(self.spell_get_triggered_spell(spell_id)) != 0) or \
                aura.affected_spell_school == DB.get_spell_school(spell_id) or aura.affected_spell_family_mask == 0:
            return True
        else:
            return False

    @lru_cache
    def spell_has_triggered_spell(self, spell_id):
        for i in range(1, 4):
            if DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell" + str(i)]] != 0:
                return True

        return False

    @lru_cache
    def spell_get_triggered_spell(self, spell_id):
        if DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell1"]] != 0:
            return DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell1"]]
        elif DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell2"]] != 0:
            return DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell2"]]
        elif DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell3"]] != 0:
            return DB.get_spell(spell_id)[DB.spell_column_info["EffectTriggerSpell3"]]
        return 0

    def on_spell_hit(self, spell_id):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.proc[1] >= random.randint(0, 100):
                    self.handle_aura_proc(aura, spell_id)

    def on_spell_crit(self, spell_id, damage=0):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.proc[1] >= random.randint(0, 100):
                    self.handle_aura_proc(aura, spell_id)

                if aura.spell_id == 11129 and aura.affected_spell_school == DB.get_spell_school(
                        spell_id):
                    self.proc_aura_charge(aura)
                elif aura.spell_id in [11119, 11120, 12846, 12847, 12848] and \
                        DB.get_spell_school(spell_id) & 4:
                    self.handle_ignite_crit(aura.spell_id, damage)
                elif aura.spell_id in [29074, 29075, 29076]:
                    self.char.current_mana += DB.get_spell(spell_id)[
                                                  DB.spell_column_info["ManaCost"]] * \
                                              (aura.value * aura.curr_stacks) / 100

    def handle_aura_proc(self, aura, spell_id):
        # proc trigger spell (11213, 12574, 12575, 12576, 12577) Clearcast proc
        if aura.spell_id not in (11180, 28592, 28593, 28594, 28595) and aura.aura_id == 42:
            self.apply_spell_effect(aura.trigger_spell)

        # scorch proc
        elif aura.spell_id in (11095, 12872, 12873) and DB.get_spell_family(spell_id) & 16:
            if aura.value >= random.randint(0, 100):
                self.apply_spell_effect(aura.trigger_spell)

        # trigger combustion aura
        elif aura.spell_id == 11129 and aura.affected_spell_school == DB.get_spell_school(spell_id):
            self.apply_spell_effect(28682)

        # frost spells apply winters chill with talent
        elif DB.get_spell_school(spell_id) == 16 and aura.spell_id in (
                11180, 28592, 28593, 28594, 28595):
            self.apply_spell_effect(aura.trigger_spell)

    def get_procable_auras(self, proc_flag):
        procced_auras = []
        for aura in self.active_auras:
            if aura.proc[0] & proc_flag or aura.proc[1] == 101:
                procced_auras.append(aura)
        return procced_auras

    def handle_ignite_crit(self, spell_id, damage):
        ignite = list(DB.get_spell(12654))

        ignite[DB.spell_column_info["EffectBasePoints1"]] = round((damage * enums.ignite_dmg_pct[spell_id] / 100) / 3) \
                                                            - 1

        self.process_dot_damage_spell(tuple(ignite), 1)

    def get_recovery_time_mod(self, spell_id):
        recovery_time_mod = 0
        # for aura in self.get_character_mod_auras(spell_id):
        for aura in self.active_auras:
            if self.aura_applies_to_spell(aura, spell_id) and \
                    (aura.aura_id == 107 and aura.misc_value == 11 and
                     (aura.spell_id not in [11078, 11080, 12342, 11165, 12475] or
                      DB.get_spell_family(spell_id) & 2 or
                      DB.get_spell_family(spell_id) & 64)):
                recovery_time_mod += aura.value * aura.curr_stacks
        return recovery_time_mod

    def get_recovery_time_multiplier(self, spell_id):
        recovery_time_multiplier = 1
        # for aura in self.get_character_mod_auras(spell_id):
        for aura in self.active_auras:
            if self.aura_applies_to_spell(aura, spell_id) and \
                    (aura.aura_id == 108 and aura.misc_value == 11 and
                     (aura.spell_id not in [11078, 11080, 12342] or DB.get_spell_family(spell_id) & 2)):
                recovery_time_multiplier *= 1 + (aura.value * aura.curr_stacks / 100)
        return recovery_time_multiplier

    def spell_start_cooldown(self, spell_id):
        if DB.get_spell(spell_id)[DB.spell_column_info["RecoveryTime"]] != 0:
            if spell_id == 11129 and not self.spell_on_cooldown(spell_id):
                ready_time = -1
            else:
                ready_time = self.env.now + \
                             DB.get_spell(spell_id)[
                                 DB.spell_column_info["RecoveryTime"]] * \
                             self.get_recovery_time_multiplier(spell_id) + \
                             self.get_recovery_time_mod(spell_id)

            self.cooldown_spell_id[spell_id] = (ready_time, DB.get_spell_school(spell_id))

        elif DB.get_spell(spell_id)[DB.spell_column_info["CategoryRecoveryTime"]] != 0:

            ready_time = self.env.now + \
                         DB.get_spell(spell_id)[
                             DB.spell_column_info["CategoryRecoveryTime"]] * \
                         self.get_recovery_time_multiplier(spell_id) + \
                         self.get_recovery_time_mod(spell_id)

            self.cooldown_spell_family_mask[DB.get_spell_family(spell_id)] = (ready_time,
                                                                              DB.get_spell_school(
                                                                                  spell_id))

    def spell_on_cooldown(self, spell_id):
        if spell_id in self.cooldown_spell_id.keys() or \
                DB.get_spell_family(spell_id) in self.cooldown_spell_family_mask.keys():
            return True
        return False

    def item_start_cooldown(self, item_id):
        for i in range(1, 6):
            if DB.get_item(item_id)[DB.item_column_info["spellcooldown_" + str(i)]] != 0:
                self.cooldown_item_id[item_id] = self.env.now \
                                                 + DB.get_item(item_id)[
                                                     DB.item_column_info["spellcooldown_" + str(i)]]
            elif DB.get_item(item_id)[DB.item_column_info["spellcategorycooldown_" + str(i)]] != 0:
                spell_category = DB.get_item(item_id)[DB.item_column_info["spellcategory_" + str(i)]]
                spell_category_cooldown = DB.get_item(item_id)[DB.item_column_info["spellcategorycooldown_" + str(i)]]
                self.cooldown_item_family_mask[spell_category] = self.env.now + spell_category_cooldown

    def item_on_cooldown(self, item_id):
        if item_id in self.cooldown_item_id.keys():
            return True
        for i in range(1, 6):
            if DB.get_item(item_id)[DB.item_column_info["spellcategory_" + str(i)]] \
                    in self.cooldown_item_family_mask.keys():
                return True
        return False

    def recover_cooldowns(self):
        for entry in dict(self.cooldown_spell_id).items():
            if entry[1][0] != -1 and entry[1][0] <= self.env.now:
                del self.cooldown_spell_id[entry[0]]

        for entry in dict(self.cooldown_spell_family_mask).items():
            if entry[1][0] != -1 and entry[1][0] <= self.env.now:
                del self.cooldown_spell_family_mask[entry[0]]

        for entry in dict(self.cooldown_item_id).items():
            if entry[1] != -1 and entry[1] <= self.env.now:
                del self.cooldown_item_id[entry[0]]

        for entry in dict(self.cooldown_item_family_mask).items():
            if entry[1] != -1 and entry[1] <= self.env.now:
                del self.cooldown_item_family_mask[entry[0]]

    def cold_snap(self, spell_id):
        for entry in dict(self.cooldown_spell_id).items():
            if entry[1][1] & 16:
                del self.cooldown_spell_id[entry[0]]
        for entry in dict(self.cooldown_spell_family_mask).items():
            if entry[1][1] & 16:
                del self.cooldown_spell_family_mask[entry[0]]
        self.spell_start_cooldown(spell_id)

    def berserking(self):
        health_pct = self.char.current_health / self.char.total_health * 100
        if health_pct <= 40:
            haste_mod = 30
        else:
            haste_mod = 10 + (100 - health_pct) / 3

        spell_info = DB.get_spell(26635)

        for i in range(1, 4):
            aura = self.get_aura(spell_info, i)
            aura.value = haste_mod
            self.active_auras.append(aura)
