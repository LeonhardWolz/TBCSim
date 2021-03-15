from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import src.db_connector as DB
from src import enums

result_line_format = "{:20s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}|{:16s}"
line_line = "----------------------------------------------------------------------------" \
            "----------------------------------------------------------------------------" \
            "-----------------------------------------------------------------------"


@dataclass
class SimResult:
    start_time: datetime
    sim_length: int
    total_damage_dealt: int = 0
    cast_spells: Dict = field(default_factory=lambda: {})
    action_order: List = field(default_factory=lambda: [])
    equipped_items: Dict = field(default_factory=lambda: {})

    def spell_cast(self, spell_id, sim_time):
        self.action_order.append((sim_time, DB.get_spell_name(spell_id) + " "
                                  + DB.get_spell(spell_id)[DB.spell_column_info["Rank1"]]))
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.casts += 1
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      casts=1)

    def damage_spell_hit(self, spell_id, damage):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.hits += 1
            spell_results.damage_dealt += damage
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      hits=1,
                                                      damage_dealt=damage)

        self.total_damage_dealt += damage

    def damage_spell_crit(self, spell_id, damage):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.crits += 1
            spell_results.damage_dealt += damage
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      crits=1,
                                                      damage_dealt=damage)

        self.total_damage_dealt += damage

    def damage_spell_resisted(self, spell_id):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.resisted += 1
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      resisted=1)

    def dot_spell_hit(self, spell_id):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.dot_hits += 1
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      dot_hits=1)

    def dot_spell_crit(self, spell_id):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.dot_crits += 1
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      dot_crits=1)

    def dot_spell_damage(self, spell_id, damage):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.dot_damage_dealt += damage
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      dot_damage_dealt=damage)

        self.total_damage_dealt += damage

    def dot_spell_resisted(self, spell_id):
        if spell_id in self.cast_spells.keys():
            spell_results = self.cast_spells.get(spell_id)
            spell_results.dot_resisted += 1
        else:
            self.cast_spells[spell_id] = SpellResults(spell_id=spell_id,
                                                      sim_length=self.sim_length,
                                                      dot_resisted=1)

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
            str_repr += "\n{:8s}| ".format(str(action[0]/1000))
            str_repr += str(action[1])

        str_repr += "\n"
        str_repr += "\n------------ Spell Cast Breakdown ------------\n\n"
        str_repr += result_line_format.format("Spell Name",
                                              "Total Casts",
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
                                              "Total DPS")
        str_repr += "\n"
        for res in self.cast_spells.values():
            str_repr += line_line + "\n"
            str_repr += str(res) + "\n"
        str_repr += line_line + "\n"
        str_repr += "Total Damage dealt: " + str(self.total_damage_dealt) + "\n"
        str_repr += "DPS: " + str(round(self.total_damage_dealt / (self.sim_length / 1000), 2)) + "\n"
        # TODO aura procs eg. Arcane Concentration

        return str_repr


@dataclass
class SpellResults:
    spell_id: int
    sim_length: int
    casts: int = 0
    hits: int = 0
    crits: int = 0
    resisted: int = 0
    damage_dealt: int = 0
    dot_hits: int = 0
    dot_crits: int = 0
    dot_resisted: int = 0
    dot_damage_dealt: int = 0

    def __str__(self):
        total_damage = self.damage_dealt + self.dot_damage_dealt
        return result_line_format.format(DB.get_spell_name(self.spell_id) + " " +
                                         DB.get_spell(self.spell_id)[DB.spell_column_info["Rank1"]],
                                         str(self.casts),
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
                                         str(round(total_damage / (self.sim_length / 1000), 2)))


@dataclass
class EquippedItem:
    name: str
    item_data: List = field(default_factory=lambda: [])

    def __str__(self):
        return self.name
