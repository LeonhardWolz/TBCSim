import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from src import enums

import src.db.sqlite_db_connector as DB

used_items_line_format = "    {:30s}|{:12s}|{:16s}"
consumable_row_divider = "    ------------------------------------------------------------"

misc_combat_action_line_format = "    {:30s}|{:12s}|{:16s}"
misc_combat_action_row_divider = "    ------------------------------------------------------------"

off_combat_action_line_format = "    {:34s}|{:8s}|{:8s}|{:8s}|{:10s}|{:10s}|{:8s}|" \
                                "{:10s}|{:10s}|{:10s}|{:12s}|{:10s}|{:12s}|{:16s}"
off_combat_action_row_divider = "    ----------------------------------------------------------------------------" \
                                "----------------------------------------------------------------------------" \
                                "---------------------------"


@dataclass
class SimResult:
    start_time: datetime
    sim_length: int
    combat_actions: Dict = field(default_factory=lambda: {})
    used_consumables: Dict = field(default_factory=lambda: {})
    action_order: List = field(default_factory=lambda: [])
    equipped_items: Dict = field(default_factory=lambda: {})
    full_combat_log: str = ""
    errors_short: str = ""

    def spell_cast(self, spell_id, spell_name, sim_time):
        self.action_order.append((sim_time, spell_name))
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.uses += 1
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     uses=1)

    def misc_effect(self, action_id, effect_strength):
        if (action_id, 1) in self.combat_actions.keys():
            self.combat_actions[(action_id, 1)].misc_effect += effect_strength
        elif (action_id, 2) in self.combat_actions.keys():
            self.combat_actions[(action_id, 2)].misc_effect += effect_strength

    def damage_spell_hit(self, spell_id, spell_name, damage):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.hits += 1
            action_result.direct_hit_damage += damage
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     hits=1,
                                                                     direct_hit_damage=damage,
                                                                     damage_action=True)

    def damage_spell_crit(self, spell_id, spell_name, damage):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.crits += 1
            action_result.direct_hit_damage += damage
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     crits=1,
                                                                     direct_hit_damage=damage,
                                                                     damage_action=True)

    def damage_spell_resisted(self, spell_id, spell_name):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.resisted += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     resisted=1,
                                                                     damage_action=True)

    def dot_spell_hit(self, spell_id, spell_name):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.dot_hits += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     dot_hits=1,
                                                                     damage_action=True)

    def dot_spell_crit(self, spell_id, spell_name):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.dot_crits += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     dot_crits=1,
                                                                     damage_action=True)

    def dot_spell_damage(self, spell_id, spell_name, damage):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.dot_damage += damage
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     dot_damage=damage,
                                                                     damage_action=True)

    def dot_spell_resisted(self, spell_id, spell_name):
        if (spell_id, 1) in self.combat_actions.keys():
            action_result = self.combat_actions.get((spell_id, 1))
            action_result.dot_resisted += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(spell_id, 1)] = CombatActionResults(attack_id=spell_id,
                                                                     attack_type=1,
                                                                     name=spell_name,
                                                                     sim_length=self.sim_length,
                                                                     dot_resisted=1,
                                                                     damage_action=True)

    def wand_attack_used(self, item_id, item_name, sim_time):
        self.action_order.append((sim_time, item_name + " wand attack"))
        if (item_id, 2) in self.combat_actions.keys():
            action_result = self.combat_actions.get((item_id, 2))
            action_result.uses += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(item_id, 2)] = CombatActionResults(attack_id=item_id,
                                                                    attack_type=2,
                                                                    name=item_name,
                                                                    sim_length=self.sim_length,
                                                                    uses=1,
                                                                    damage_action=True)

    def wand_attack_hit(self, item_id, item_name, damage):
        if (item_id, 2) in self.combat_actions.keys():
            action_result = self.combat_actions.get((item_id, 2))
            action_result.hits += 1
            action_result.direct_hit_damage += damage
            action_result.damage_action = True
        else:
            self.combat_actions[(item_id, 2)] = CombatActionResults(attack_id=item_id,
                                                                    attack_type=2,
                                                                    name=item_name,
                                                                    sim_length=self.sim_length,
                                                                    hits=1,
                                                                    direct_hit_damage=damage,
                                                                    damage_action=True)

    def wand_attack_crit(self, item_id, item_name, damage):
        if (item_id, 2) in self.combat_actions.keys():
            action_result = self.combat_actions.get((item_id, 2))
            action_result.crits += 1
            action_result.direct_hit_damage += damage
            action_result.damage_action = True
        else:
            self.combat_actions[(item_id, 2)] = CombatActionResults(attack_id=item_id,
                                                                    attack_type=1,
                                                                    name=item_name,
                                                                    sim_length=self.sim_length,
                                                                    crits=1,
                                                                    direct_hit_damage=damage,
                                                                    damage_action=True)

    def wand_attack_resisted(self, item_id, item_name):
        if (item_id, 2) in self.combat_actions.keys():
            action_result = self.combat_actions.get((item_id, 2))
            action_result.resisted += 1
            action_result.damage_action = True
        else:
            self.combat_actions[(item_id, 2)] = CombatActionResults(attack_id=item_id,
                                                                    attack_type=1,
                                                                    name=item_name,
                                                                    sim_length=self.sim_length,
                                                                    resisted=1,
                                                                    damage_action=True)

    def item_used(self, item_id, item_name, sim_time):
        self.action_order.append((sim_time, "Used " + item_name))
        if item_id in self.used_consumables.keys():
            used_consumable = self.used_consumables.get(item_id)
            used_consumable.uses += 1
        else:
            self.used_consumables[item_id] = UsedConsumable(name=item_name,
                                                            item_id=item_id,
                                                            uses=1)

    def item_mana_restored(self, item_id, mana_restored):
        if item_id in self.used_consumables.keys():
            self.used_consumables.get(item_id).mana_restored += mana_restored

    def set_items(self, items):
        self.equipped_items = items

    def info(self, log_str):
        self.full_combat_log += time.strftime("%Y/%m/%d-%H:%M:%S") + f": INFO {log_str}\n"

    def logg(self, log_str):
        self.full_combat_log += time.strftime("%Y/%m/%d-%H:%M:%S") + f": {log_str}\n"

    def warning(self, warning_str):
        self.full_combat_log += time.strftime("%Y/%m/%d-%H:%M:%S") + f": WARNING {warning_str}\n"

    @property
    def dps(self):
        return round(self.total_damage_dealt / (self.sim_length / 1000), 2)

    @property
    def total_damage_dealt(self):
        return sum([res.total_damage for res in self.combat_actions.values()])

    def __str__(self):
        str_repr = "\n    TBC Combat Simulation from: {}\n\n".format(self.start_time.strftime("%Y-%m-%d %H:%M:%S"))

        str_repr += "    ------------ Action Order ------------\n\n"

        str_repr += "    Simtime | Combat Action\n"
        str_repr += "    ---------------------------------"
        for action in self.action_order:
            str_repr += f"\n    {action[0] / 1000:7.3f} | {action[1]}"

        str_repr += "\n"
        str_repr += "\n    --------------- Item Combat Action Breakdown ---------------\n\n"
        str_repr += used_items_line_format.format("Item Name",
                                                  "Total Uses",
                                                  "Mana restored")
        str_repr += "\n"
        for consumable in self.used_consumables.values():
            str_repr += consumable_row_divider + "\n"
            str_repr += str(consumable) + "\n"
        str_repr += consumable_row_divider + "\n"

        str_repr += "\n"
        str_repr += "\n    --------------- Misc Combat Action Breakdown ---------------\n\n"
        str_repr += misc_combat_action_line_format.format("Combat Action Name",
                                                          "Total Uses",
                                                          "Misc Effect")
        str_repr += "\n"
        for res in self.combat_actions.values():
            if not res.damage_action:
                str_repr += misc_combat_action_row_divider + "\n"
                str_repr += misc_combat_action_line_format.format(str(res.name),
                                                                  str(res.uses),
                                                                  str(res.misc_effect)) + "\n"
        str_repr += misc_combat_action_row_divider + "\n"

        str_repr += "\n"
        str_repr += "\n    ------------ Offensive Combat Action Breakdown ------------\n\n"
        str_repr += off_combat_action_line_format.format("Combat Action Name",
                                                         "Uses",
                                                         "Hits",
                                                         "Crits",
                                                         "Resisted",
                                                         "Damage",
                                                         "DPS",
                                                         "Dot Hits",
                                                         "Dot Crits",
                                                         "Dot Res.",
                                                         "Dot Damage",
                                                         "Dot DPS",
                                                         "Total DPS",
                                                         "Misc Effect")
        str_repr += "\n"
        combat_actions = list(self.combat_actions.values())
        combat_actions.sort(key=lambda x: x.total_dps, reverse=True)
        for res in combat_actions:
            if res.damage_action:
                str_repr += off_combat_action_row_divider + "\n"
                str_repr += str(res) + "\n"
        str_repr += off_combat_action_row_divider + "\n"
        str_repr += "    Total Damage dealt: " + str(self.total_damage_dealt) + "\n"
        str_repr += "    DPS: " + str(self.dps) + "\n"
        # TODO aura procs ie. Arcane Concentration

        return str_repr


@dataclass
class CombatActionResults:
    attack_id: int
    attack_type: int  # 1= spell, 2=wand attack
    name: str
    sim_length: int
    damage_action: bool = False
    uses: int = 0
    hits: int = 0
    crits: int = 0
    resisted: int = 0
    direct_hit_damage: int = 0
    dot_hits: int = 0
    dot_crits: int = 0
    dot_resisted: int = 0
    dot_damage: int = 0
    misc_effect: int = 0

    @property
    def total_damage(self):
        return self.direct_hit_damage + self.dot_damage

    def __str__(self):
        return off_combat_action_line_format.format(self.name,
                                                    str(self.uses),
                                                    str(self.hits),
                                                    str(self.crits),
                                                    str(self.resisted),
                                                    str(self.direct_hit_damage),
                                                    str(self.direct_hit_dps),
                                                    str(self.dot_hits),
                                                    str(self.dot_crits),
                                                    str(self.dot_resisted),
                                                    str(self.dot_damage),
                                                    str(self.dot_dps),
                                                    str(self.total_dps),
                                                    str(self.misc_effect))

    @property
    def direct_hit_dps(self):
        return round(self.direct_hit_damage / (self.sim_length / 1000), 2)

    @property
    def dot_dps(self):
        return round(self.dot_damage / (self.sim_length / 1000), 2)

    @property
    def total_dps(self):
        return round(self.total_damage / (self.sim_length / 1000), 2)


@dataclass
class EquippedItem:
    name: str
    item_data: List = field(default_factory=lambda: [])
    enchantment: str = ""
    sockets: List = field(default_factory=lambda: [])
    socket_bonus: int = None
    socket_bonus_met: bool = False

    def __str__(self):
        str_repr = "\n\tName:\t\t" + self.name
        if self.enchantment != "":
            str_repr += "\n\tEnchantment:\t" + self.enchantment

        if self.sockets:
            str_repr += "\n\tSockets:"
            for socket in self.sockets:
                str_repr += "\n\t\t" + enums.socket_color_name[socket[0]] + " Socket: \t\t"
                if socket[2] is not None:
                    str_repr += str(socket[2]) + ": " + str(socket[3])
                    if socket[1] & 1 and socket[4]:
                        str_repr += " - Gem Active"
                    elif socket[1] & 1 and not socket[4]:
                        str_repr += " - Gem Inactive"
                else:
                    str_repr += "Socket Empty"
        if self.socket_bonus != 0:
            socket_bonus_name = DB.get_enchant(self.socket_bonus)[DB.enchant_column_info["m_name_lang_1"]]
            str_repr += f"\n\t\tSocket Bonus {'Active' if self.socket_bonus_met else 'Inactive'}: \t{socket_bonus_name}"
        return str_repr


@dataclass
class UsedConsumable:
    name: str
    item_id: int
    uses: int = 0
    mana_restored: int = 0

    def __str__(self):
        return used_items_line_format.format(self.name,
                                             str(self.uses),
                                             str(self.mana_restored))
