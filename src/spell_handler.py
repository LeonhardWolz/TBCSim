import logging
import random
import src.db_connector as DB

from src import enums
from src.aura import Aura
from src.dot import Dot


class SpellHandler:
    cooldown_spell_id = {}
    cooldown_family_mask = {}

    def __init__(self, char):
        self.char = char
        self.active_auras = []
        self.enemy = None
        self.env = None
        self.results = None
        self.logger = logging.getLogger("simulation")

    def apply_spell_effect(self, spell_id):
        spell_info = DB.get_spell(spell_id)
        for j in range(1, 4):
            if spell_info[DB.spell_column_info["Effect" + str(j)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 6:
                # Deal spell school damage to enemy
                self.process_direct_damage_spell(spell_info, j)

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] == 2 and \
                    spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(j)]] == 1:

                # Deal spell school damage to character
                raise NotImplementedError("Damage to character not implemented")

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

            elif spell_info[DB.spell_column_info["Effect" + str(j)]] != 0:
                logging.warning("Effect " + str(j) + " of Spell could not be handled: " + str(spell_info))

    def apply_passive_auras(self, spell_info, effect_slot):

        if spell_info[DB.spell_column_info["EffectImplicitTargetA" + str(effect_slot)]] == 1:
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
                    aura.create_time = self.env.now
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
        value = self.get_effect_strength(spell_info, effect_slot)
        aura_id = spell_info[DB.spell_column_info["EffectApplyAuraName" + str(effect_slot)]]
        misc_value = spell_info[DB.spell_column_info["EffectMiscValue" + str(effect_slot)]]

        # Increase clearcasting crit chance from Arcane Potency
        if spell_info[0] == 12536 and aura_id == 57:
            for aura in [aura for aura in self.active_auras if aura.spell_id in [31571, 31572, 31573]]:
                value += aura.value

        affected_spell_school = spell_info[DB.spell_column_info["SchoolMask"]]
        affected_spell_family_mask = DB.get_spell_family_affected(spell_info[0])

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

        if affected_spell_family_mask is not None and affected_spell_family_mask[1] == (effect_slot - 1):
            return Aura(value=value,
                        spell_id=spell_info[0],
                        aura_id=aura_id,
                        misc_value=misc_value,
                        stack_limit=stack_limit,
                        affected_spell_school=affected_spell_school,
                        affected_spell_family_mask=affected_spell_family_mask[2],
                        create_time=create_time,
                        duration_index=duration_index,
                        trigger_spell=trigger_spell,
                        proc=proc,
                        attributes=attributes)

        return Aura(value=value,
                    spell_id=spell_info[0],
                    aura_id=aura_id,
                    misc_value=misc_value,
                    stack_limit=stack_limit,
                    affected_spell_school=affected_spell_school,
                    create_time=create_time,
                    duration_index=duration_index,
                    trigger_spell=trigger_spell,
                    proc=proc,
                    attributes=attributes)

    def get_effect_strength(self, spell_info, effect_slot):
        min_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * 1
        max_value = spell_info[DB.spell_column_info["EffectBasePoints" + str(effect_slot)]] + \
                    spell_info[DB.spell_column_info["EffectBaseDice" + str(effect_slot)]] * \
                    spell_info[DB.spell_column_info["EffectDieSides" + str(effect_slot)]]
        return random.randint(min_value, max_value)

    def spell_dot_behaviour(self, spell_info, effect_slot):
        return enums.duration_index[spell_info[DB.spell_column_info["DurationIndex"]]], \
               spell_info[DB.spell_column_info["EffectAmplitude" + str(effect_slot)]]

    def spell_mana_cost(self, spell_id):
        return DB.get_spell(spell_id)[DB.spell_column_info["ManaCost"]]

    def spell_cast_time(self, spell_id):
        return enums.cast_time[DB.get_spell(spell_id)[DB.spell_column_info["CastingTimeIndex"]]]

    def spell_power_coefficient(self, spell_id):
        # TODO improve: eg. spells that apply auras sometimes have a 0.95 multiplier
        # Instant Spells are counted as 1.5s casts. casts longer than 7s are considered 7s casts
        coeff_cast_time = min(
            max(enums.cast_time[DB.get_spell(spell_id)[DB.spell_column_info["CastingTimeIndex"]]], 1500),
            7000)
        return coeff_cast_time / 3500

    def spell_family_mask(self, spell_id):
        return DB.get_spell(spell_id)[DB.spell_column_info["SpellFamilyFlags"]]

    def spell_does_hit(self, spell_id):
        # TODO consider player and enemy level. currently player=70 enemy=73 boss
        return random.uniform(0.00, 100.00) < (83 + self.char.spell_hit_chance_spell(spell_id))

    def spell_crit(self, spell_id):
        return random.uniform(0.00, 100.00) < self.char.spell_crit_chance_spell(spell_id)

    def process_direct_damage_spell(self, spell_info, effect_slot):
        if self.spell_does_hit(spell_info[0]):
            spell_base_damage = self.get_effect_strength(spell_info, effect_slot)
            spell_spell_power = self.char.spell_spell_power(spell_info[0])
            spell_power_coefficient = self.char.spell_power_coefficient(spell_info[0])
            spell_damage_multiplier = self.char.spell_dmg_multiplier(spell_info[0])

            spell_damage = round((spell_base_damage + spell_spell_power * spell_power_coefficient)
                                 * spell_damage_multiplier)

            if self.spell_crit(spell_info[0]):
                spell_damage *= self.char.spell_crit_dmg_multiplier(spell_info[0])
                spell_damage = round(spell_damage)
                self.on_spell_crit(spell_info[0], spell_damage)
                self.logg(DB.get_spell_name(spell_info[0]) + " critical damage: " + str(spell_damage))
                self.results.damage_spell_crit(spell_info[0], spell_damage)
            else:
                self.on_spell_hit(spell_info[0])
                self.logg(DB.get_spell_name(spell_info[0]) + " damage: " + str(spell_damage))
                self.results.damage_spell_hit(spell_info[0], spell_damage)
            self.on_damage(spell_info)
        else:
            self.logg(DB.get_spell_name(spell_info[0]) + " resisted")
            self.results.damage_spell_resisted(spell_info[0])

    def process_dot_damage_spell(self, spell_info, effect_slot):
        # TODO Consider all Character Stats for damage
        if self.spell_does_hit(spell_info[0]):
            dot_duration, dot_interval = self.spell_dot_behaviour(spell_info, effect_slot)
            dot_damage = round(self.get_effect_strength(spell_info, effect_slot) *
                               self.enemy_damage_taken_mod(spell_info[0]))

            self.env.process(Dot(self.env,
                                 self,
                                 spell_info[0],
                                 dot_damage,
                                 dot_interval,
                                 dot_duration,
                                 self.results).ticking())
        else:
            self.logg(DB.get_spell_name(spell_info[0]) + " dot resisted")
            self.results.dot_spell_resisted(spell_info[0])

    def enemy_damage_taken_mod(self, spell_id):
        dmg_taken_mod = 1
        for aura in self.get_enemy_mod_auras(spell_id):
            if aura.aura_id == 87 and \
                    aura.affected_spell_school & DB.get_spell(spell_id)[DB.spell_column_info["SchoolMask"]]:
                dmg_taken_mod *= 1 + (aura.value * aura.curr_stacks / 100)

        return dmg_taken_mod

    def curr_sim_time_str(self):
        return str(self.env.now / 1000)

    def remove_expired_auras(self):
        for aura in self.active_auras:
            if self.env.now - aura.create_time > enums.duration_index[aura.duration_index] != -1:
                self.active_auras.remove(aura)

    def proc_aura_charge(self, aura):
        aura.procced()
        if aura.proc[2] - aura.proc_counter == 0:
            # Handle Combustion Auras
            if aura.spell_id == 11129:
                self.remove_auras_from_spell(28682)
            self.active_auras.remove(aura)

    def remove_auras_from_spell(self, spell_id):
        for aura in self.active_auras[:]:
            if aura.spell_id == spell_id:
                self.active_auras.remove(aura)

    def logg(self, info):
        self.logger.info("{:8s} {}".format(self.curr_sim_time_str(), info))

    def on_damage(self, spell_info):
        # Mage
        if spell_info[DB.spell_column_info["SpellFamilyName"]] == 3:
            # Arcane Blast
            if spell_info[DB.spell_column_info["SpellFamilyFlags"]] & 0x20000000:
                self.apply_spell_effect(36032)

    def get_spell_gcd(self, spell_id):
        return DB.get_spell_gcd(spell_id)

    def get_character_mod_auras(self, spell_id):
        mod_auras = []
        for aura in self.active_auras:
            if self.aura_applies_to_spell(aura, spell_id):
                mod_auras.append(aura)
        return mod_auras

    def get_enemy_mod_auras(self, spell_id):
        mod_auras = []
        for aura in self.enemy.active_auras:
            if self.aura_applies_to_spell(aura, spell_id):
                mod_auras.append(aura)
        return mod_auras

    def aura_applies_to_spell(self, aura, spell_id):
        if aura.affected_spell_family_mask & self.spell_family_mask(spell_id) != 0 or \
                aura.affected_spell_school == DB.get_spell_school(spell_id) or aura.affected_spell_family_mask == 0:
            return True
        else:
            return False

    def on_spell_hit(self, spell_id):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.proc[1] > random.randint(0, 100):
                    self.handle_aura_proc(aura, spell_id)

    def on_spell_crit(self, spell_id, damage=0):
        for aura in self.get_procable_auras(proc_flag=65536):
            if self.aura_applies_to_spell(aura, spell_id):
                if aura.proc[1] > random.randint(0, 100):
                    self.handle_aura_proc(aura, spell_id)

                if aura.spell_id == 11129 and aura.affected_spell_school == DB.get_spell_school(spell_id):
                    self.proc_aura_charge(aura)
                elif aura.spell_id in [11119, 11120, 12846, 12847, 12848]:
                    self.handle_ignite_crit(aura.spell_id, damage)
                elif aura.spell_id in [29074, 29075, 29076]:
                    self.char.current_mana += DB.get_spell(spell_id)[DB.spell_column_info["ManaCost"]] * \
                                              (aura.value * aura.curr_stacks) / 100

    def handle_aura_proc(self, aura, spell_id):
        # proc trigger spell
        if aura.spell_id in [11213, 12574, 12575, 12576, 12577] and aura.aura_id == 42:
            self.apply_spell_effect(aura.trigger_spell)

        # scorch proc
        if aura.spell_id in (11095, 12872, 12873):
            if aura.value >= random.randint(0, 100):
                self.apply_spell_effect(aura.trigger_spell)

        # trigger combustion aura
        if aura.spell_id == 11129 and aura.affected_spell_school == DB.get_spell_school(spell_id):
            self.apply_spell_effect(28682)

        # frost spells apply winters chill with talent
        if DB.get_spell_school(spell_id) == 16:
            for aura in self.active_auras:
                if aura.spell_id in [11180, 28592, 28593, 28594, 28595]:
                    self.apply_spell_effect(aura.trigger_spell)

    def get_procable_auras(self, proc_flag):
        procced_auras = []
        for aura in self.active_auras:
            if aura.proc[0] & proc_flag or aura.proc[1] == 101:
                procced_auras.append(aura)
        return procced_auras

    def handle_ignite_crit(self, spell_id, damage):
        ignite = list(DB.get_spell(12654))
        ignite_dmg_pct = 0
        if spell_id == 11119:
            ignite_dmg_pct = 8
        elif spell_id == 11120:
            ignite_dmg_pct = 16
        elif spell_id == 12846:
            ignite_dmg_pct = 24
        elif spell_id == 12847:
            ignite_dmg_pct = 32
        elif spell_id == 12848:
            ignite_dmg_pct = 40

        ignite[DB.spell_column_info["EffectBasePoints1"]] = round(damage * (ignite_dmg_pct / 100) - 1)

        self.process_dot_damage_spell(ignite, 1)

    def get_recovery_time_mod(self, spell_id):
        recovery_time_mod = 0
        for aura in self.get_character_mod_auras(spell_id):
            if aura.aura_id == 107 and aura.misc_value == 11:
                recovery_time_mod += aura.value * aura.curr_stacks
        return recovery_time_mod

    def get_recovery_time_multiplier(self, spell_id):
        recovery_time_multiplier = 1
        for aura in self.get_character_mod_auras(spell_id):
            if aura.aura_id == 108 and aura.misc_value == 11:
                recovery_time_multiplier *= 1 + (aura.value * aura.curr_stacks / 100)
        return recovery_time_multiplier

    def spell_start_cooldown(self, spell_id):
        # if self.spell_family_mask(spell_id) == 0 and \
        #         DB.get_spell(spell_id)[DB.spell_column_info["RecoveryTime"]] != 0:
        if DB.get_spell(spell_id)[DB.spell_column_info["RecoveryTime"]] != 0:

            ready_time = self.env.now + \
                         DB.get_spell(spell_id)[DB.spell_column_info["RecoveryTime"]] * \
                         self.get_recovery_time_multiplier(spell_id) + \
                         self.get_recovery_time_mod(spell_id)

            self.cooldown_spell_id[spell_id] = ready_time
        # elif self.spell_family_mask(spell_id) != 0 and \
        #         DB.get_spell(spell_id)[DB.spell_column_info["CategoryRecoveryTime"]]:
        elif DB.get_spell(spell_id)[DB.spell_column_info["CategoryRecoveryTime"]] != 0:

            ready_time = self.env.now + \
                         DB.get_spell(spell_id)[DB.spell_column_info["CategoryRecoveryTime"]] * \
                         self.get_recovery_time_multiplier(spell_id) + \
                         self.get_recovery_time_mod(spell_id)

            self.cooldown_family_mask[self.spell_family_mask(spell_id)] = ready_time

    def spell_on_cooldown(self, spell_id):
        if spell_id in self.cooldown_spell_id.keys() or \
                self.spell_family_mask(spell_id) in self.cooldown_family_mask.keys():
            return True
        return False

    def recover_cooldowns(self):
        for entry in dict(self.cooldown_spell_id).items():
            if entry[1] <= self.env.now:
                del self.cooldown_spell_id[entry[0]]
        for entry in dict(self.cooldown_family_mask).items():
            if entry[1] <= self.env.now:
                del self.cooldown_family_mask[entry[0]]
