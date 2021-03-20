from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import src.db_connector as DB
from src import enums

spell_result_line_format = "{:24s}|{:12s}|{:12s}|{:12s}|{:16s}|{:14s}|{:8s}|" \
                           "{:16s}|{:16s}|{:14s}|{:16s}|{:8s}|{:10s}|{:16s}"
spell_row_divider = "----------------------------------------------------------------------------" \
                    "----------------------------------------------------------------------------" \
                    "-----------------------------------------------------------------------"

used_consumables_line_format = "{:24s}|{:16s}|{:16s}"
consumable_row_divider = "----------------------------------------------------------"


@dataclass
class SimResult:
    start_time: datetime
    sim_length: int
    total_damage_dealt: int = 0
    used_attacks: Dict = field(default_factory=lambda: {})
    used_consumables: Dict = field(default_factory=lambda: {})
    action_order: List = field(default_factory=lambda: [])
    equipped_items: Dict = field(default_factory=lambda: {})

    def spell_cast(self, spell_id, sim_time):
        self.action_order.append((sim_time, DB.get_spell_name(spell_id) + " "
                                  + DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]]))
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.uses += 1
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             uses=1)

    def misc_effect(self, action_id, effect_strength):
        if (action_id, 1) in self.used_attacks.keys():
            self.used_attacks[(action_id, 1)].misc_effect += effect_strength
        elif (action_id, 2) in self.used_attacks.keys():
            self.used_attacks[(action_id, 2)].misc_effect += effect_strength

    def damage_spell_hit(self, spell_id, damage):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.hits += 1
            action_result.damage_dealt += damage
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             hits=1,
                                                             damage_dealt=damage)

        self.total_damage_dealt += damage

    def damage_spell_crit(self, spell_id, damage):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.crits += 1
            action_result.damage_dealt += damage
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             crits=1,
                                                             damage_dealt=damage)

        self.total_damage_dealt += damage

    def damage_spell_resisted(self, spell_id):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.resisted += 1
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             resisted=1)

    def dot_spell_hit(self, spell_id):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.dot_hits += 1
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             dot_hits=1)

    def dot_spell_crit(self, spell_id):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.dot_crits += 1
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             dot_crits=1)

    def dot_spell_damage(self, spell_id, damage):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.dot_damage_dealt += damage
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             dot_damage_dealt=damage)

        self.total_damage_dealt += damage

    def dot_spell_resisted(self, spell_id):
        if (spell_id, 1) in self.used_attacks.keys():
            action_result = self.used_attacks.get((spell_id, 1))
            action_result.dot_resisted += 1
        else:
            self.used_attacks[(spell_id, 1)] = DamageResults(attack_id=spell_id,
                                                             attack_type=1,
                                                             name=DB.get_spell_name(spell_id) + " " +
                                                                  DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]],
                                                             sim_length=self.sim_length,
                                                             dot_resisted=1)

    def wand_attack_used(self, item_id, sim_time):
        self.action_order.append((sim_time, DB.get_item_name(item_id) + " wand attack"))
        if (item_id, 2) in self.used_attacks.keys():
            action_result = self.used_attacks.get((item_id, 2))
            action_result.uses += 1
        else:
            self.used_attacks[(item_id, 2)] = DamageResults(attack_id=item_id,
                                                            attack_type=2,
                                                            name=DB.get_item_name(item_id),
                                                            sim_length=self.sim_length,
                                                            uses=1)

    def wand_attack_hit(self, item_id, damage):
        if (item_id, 2) in self.used_attacks.keys():
            action_result = self.used_attacks.get((item_id, 2))
            action_result.hits += 1
            action_result.damage_dealt += damage
        else:
            self.used_attacks[(item_id, 2)] = DamageResults(attack_id=item_id,
                                                            attack_type=2,
                                                            name=DB.get_item_name(item_id),
                                                            sim_length=self.sim_length,
                                                            hits=1,
                                                            damage_dealt=damage)

        self.total_damage_dealt += damage

    def wand_attack_crit(self, item_id, damage):
        if (item_id, 2) in self.used_attacks.keys():
            action_result = self.used_attacks.get((item_id, 2))
            action_result.crits += 1
            action_result.damage_dealt += damage
        else:
            self.used_attacks[(item_id, 2)] = DamageResults(attack_id=item_id,
                                                            attack_type=1,
                                                            name=DB.get_item_name(item_id),
                                                            sim_length=self.sim_length,
                                                            crits=1,
                                                            damage_dealt=damage)

        self.total_damage_dealt += damage

    def wand_attack_resisted(self, item_id):
        if (item_id, 2) in self.used_attacks.keys():
            action_result = self.used_attacks.get((item_id, 2))
            action_result.resisted += 1
        else:
            self.used_attacks[(item_id, 2)] = DamageResults(attack_id=item_id,
                                                            attack_type=1,
                                                            name=DB.get_item_name(item_id),
                                                            sim_length=self.sim_length,
                                                            resisted=1)

    def item_used(self, item_id, sim_time):
        self.action_order.append((sim_time, "Used " + DB.get_item_name(item_id)))
        if item_id in self.used_consumables.keys():
            used_consumable = self.used_consumables.get(item_id)
            used_consumable.uses += 1
        else:
            self.used_consumables[item_id] = UsedConsumable(name=DB.get_item_name(item_id),
                                                            item_id=item_id,
                                                            uses=1)

    def item_mana_restored(self, item_id, mana_restored):
        if item_id in self.used_consumables.keys():
            self.used_consumables.get(item_id).mana_restored += mana_restored

    def set_items(self, items):
        self.equipped_items = items

    def __str__(self):
        str_repr = "Results for TBC Damage Simulation from: {}\n\n".format(
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"))
        str_repr += "Length of Simulation: {}s\n\n".format(str(self.sim_length / 1000))

        str_repr += "------------ Equipped Items ------------\n\n"

        for i in range(0, 20):
            str_repr += "{:9s}: ".format(enums.inventory_slot[i])
            if i in self.equipped_items.keys():
                str_repr += str(self.equipped_items.get(i))
            else:
                str_repr += "----"

            str_repr += "\n"

        str_repr += "\n------------ Action Order ------------\n\n"

        str_repr += "Simtime   Combat Action\n"
        str_repr += "---------------------------------"
        for action in self.action_order:
            str_repr += "\n{:8s}| ".format(str(action[0] / 1000))
            str_repr += str(action[1])

        str_repr += "\n"
        str_repr += "\n------------ Consumable Breakdown ------------\n\n"
        str_repr += used_consumables_line_format.format("Consumable Name",
                                                        "Total Uses",
                                                        "Mana restored")
        str_repr += "\n"
        for consumable in self.used_consumables.values():
            str_repr += consumable_row_divider + "\n"
            str_repr += str(consumable) + "\n"
        str_repr += consumable_row_divider + "\n"

        str_repr += "\n------------ Spell Action Breakdown ------------\n\n"
        str_repr += spell_result_line_format.format("Spell Action Name",
                                                    "Total Uses",
                                                    "Total Hits",
                                                    "Total Crits",
                                                    "Total Resisted",
                                                    "Total Damage",
                                                    "DPS",
                                                    "Total Dot Hits",
                                                    "Total Dot Crits",
                                                    "Total Dot Res.",
                                                    "Total Dot Damage",
                                                    "Dot DPS",
                                                    "Total DPS",
                                                    "Misc Effect (eg. Mana Restored)")
        str_repr += "\n"
        for res in self.used_attacks.values():
            str_repr += spell_row_divider + "\n"
            str_repr += str(res) + "\n"
        str_repr += spell_row_divider + "\n"
        str_repr += "Total Damage dealt: " + str(self.total_damage_dealt) + "\n"
        str_repr += "DPS: " + str(round(self.total_damage_dealt / (self.sim_length / 1000), 2)) + "\n"
        # TODO aura procs eg. Arcane Concentration

        return str_repr


@dataclass
class DamageResults:
    attack_id: int
    attack_type: int  # 1= spell, 2=wand attack
    name: str
    sim_length: int
    uses: int = 0
    hits: int = 0
    crits: int = 0
    resisted: int = 0
    damage_dealt: int = 0
    dot_hits: int = 0
    dot_crits: int = 0
    dot_resisted: int = 0
    dot_damage_dealt: int = 0
    misc_effect: int = 0

    def __str__(self):
        total_damage = self.damage_dealt + self.dot_damage_dealt
        return spell_result_line_format.format(self.name,
                                               str(self.uses),
                                               str(self.hits),
                                               str(self.crits),
                                               str(self.resisted),
                                               str(self.damage_dealt),
                                               str(round(self.damage_dealt / (self.sim_length / 1000), 2)),
                                               str(self.dot_hits),
                                               str(self.dot_crits),
                                               str(self.dot_resisted),
                                               str(self.dot_damage_dealt),
                                               str(round(self.dot_damage_dealt / (self.sim_length / 1000), 2)),
                                               str(round(total_damage / (self.sim_length / 1000), 2)),
                                               str(self.misc_effect))


@dataclass
class EquippedItem:
    name: str
    item_data: List = field(default_factory=lambda: [])

    def __str__(self):
        return self.name


@dataclass
class UsedConsumable:
    name: str
    item_id: int
    uses: int = 0
    mana_restored: int = 0

    def __str__(self):
        return used_consumables_line_format.format(self.name,
                                                   str(self.uses),
                                                   str(self.mana_restored))
