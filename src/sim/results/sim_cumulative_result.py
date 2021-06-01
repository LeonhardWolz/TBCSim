import os
from dataclasses import dataclass
from math import sqrt

from src import enums
import src.db.sqlite_db_connector as DB

row_divider = "---------------------------------------------------------------" \
              "---------------------------------------------------------------"


@dataclass
class SimCumResult:
    def __init__(self):
        self.settings = None
        self.results = []
        self.start_time = None
        self.run_time = None
        self.errors = []
        self.char = []

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def run_time(self):
        return self._run_time

    @run_time.setter
    def run_time(self, value):
        self._run_time = value

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value

    def all_errors_short(self):
        return self.errors + [result.errors_short for result in [result[0] for result in self.results] if
                              result.errors_short != ""]

    def __str__(self):
        str_repr = "Results for TBC Combat Simulation from: {}\n\n".format(
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"))

        str_repr += "---------------------- Simulation Settings --------------------\n"
        str_repr += f"Simulation Type: {self.settings.sim_type}\n"
        str_repr += f"Length of Simulation: {str(self.settings.sim_duration / 1000)}s\n"
        str_repr += f"Iterations: {self.settings.sim_iterations}\n"
        str_repr += f"Combat Action Rater: {self.settings.sim_combat_rater}\n\n"

        for index, character in enumerate(self.char):

            str_repr += "\n\n"
            str_repr += "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
            str_repr += f"                   SIMULATION NO. {str(index+1)}\n"
            str_repr += "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n"

            str_repr += "---------------------- Character Info --------------------\n"
            str_repr += f"{'Race:':20} {character.race}\n"
            str_repr += f"{'Class:':20} {character.player_class}\n"
            str_repr += f"{'Level:':20} {character.level}\n"
            str_repr += f"{'Talents:':20} {character.talents}\n"

            str_repr += f"\n---------------------- Active Damage Spells ----------------------\n"
            for spell_id in character.damage_spells:
                spell_info = DB.get_spell(spell_id)
                name = spell_info[DB.spell_column_info["SpellName"]] + " " + \
                       (spell_info[DB.spell_column_info["Rank1"]] or "")
                str_repr += f"{spell_id:6} {name}\n"

            str_repr += f"\n---------------------- Passive Spells ----------------------\n"
            for spell_id in character.passive_spells:
                spell_info = DB.get_spell(spell_id)
                name = spell_info[DB.spell_column_info["SpellName"]] + " " + \
                       (spell_info[DB.spell_column_info["Rank1"]] or "")
                str_repr += f"{spell_id:6} {name}\n"

            str_repr += f"\n---------------------- Active Items ----------------------\n"
            for item_id in character.active_consumables.keys():
                item_info = DB.get_item(item_id)
                name = item_info[DB.item_column_info["name"]]
                str_repr += f"{item_id:6} {name}\n"

            str_repr += f"\n---------------------- Passive Items ----------------------\n"
            for item_id in character.passive_consumables:
                item_info = DB.get_item(item_id)
                name = item_info[DB.item_column_info["name"]]
                str_repr += f"{item_id:6} {name}\n"

            str_repr += "\n---------------------- Equipped Items ----------------------\n\n"
            for i in range(0, 20):
                if i in enums.inventory_slot:
                    str_repr += f"  {enums.inventory_slot[i]:10s}: "
                    if i in character.gear.keys():
                        str_repr += str(character.gear.get(i)) + "\n"
                    else:
                        str_repr += "----\n"
                    str_repr += "-------------------------------------------------------------------------------\n"

            str_repr += "\n"

            str_repr += "---------------------- Stats from Gear,Talents and Buffs --------------------\n"
            str_repr += f"{'Health:':20} {character.total_health}\n"
            str_repr += f"{'Mana:':20} {character.total_mana}\n"
            str_repr += f"{'MP5:':20} {character.total_mp5}\n"
            str_repr += f"{'Agility:':20} {character.total_agility}\n"
            str_repr += f"{'Strength:':20} {character.total_strength}\n"
            str_repr += f"{'Intellect:':20} {character.total_intellect}\n"
            str_repr += f"{'Spirit:':20} {character.total_spirit}\n"
            str_repr += f"{'Stamina:':20} {character.total_stamina}\n"
            str_repr += f"{'Spell Crit Rating:':20} {character.total_spell_crit_rating}\n"
            str_repr += f"{'Spell Hit Rating:':20} {character.total_spell_hit_rating}\n"
            str_repr += f"{'Spell Haste Rating:':20} {character.spell_haste_rating}\n"
            str_repr += f"{'Spell Crit Chance:':20} {character.spell_crit_chance}\n"
            str_repr += f"{'Spell Hit Chance:':20} {character.spell_hit_chance}\n"
            str_repr += f"{'Spell Haste Percent:':20} {character.spell_haste_percent}\n"
            str_repr += f"{'Holy Power:':20} {character.total_holy_power}\n"
            str_repr += f"{'Fire Power:':20} {character.total_fire_power}\n"
            str_repr += f"{'Nature Power:':20} {character.total_nature_power}\n"
            str_repr += f"{'Frost Power:':20} {character.total_frost_power}\n"
            str_repr += f"{'Shadow Power:':20} {character.total_shadow_power}\n"
            str_repr += f"{'Arcane Power:':20} {character.total_arcane_power}\n"

            str_repr += "\nBest Single Simulation by DPS Results:\n"
            str_repr += row_divider
            str_repr += str(max(self.results[index], key=lambda res: res.dps))
            str_repr += row_divider

        for index, result in enumerate(self.results):
            str_repr += f"\n\n----------------------------- " \
                        f"Sim Results for Simulation {str(index+1)} -----------------------------\n"
            str_repr += f"Completed {self.settings.sim_iterations} iterations of " \
                        f"{self.settings.sim_duration / 1000} seconds in {self.run_time/2} seconds\n\n"
            str_repr += f"90% Confidence Margin of Error\n"
            str_repr += f"Avg DPS: {self.avg_dps(index)} +-{self.margin_of_error(index)}\n"
            str_repr += f"Standard deviation: {self.standard_deviation(index)}\n"

        if self.errors:
            str_repr += "\n\n---------------------- Errors during Simulation --------------------\n"
            for x, error in enumerate(self.all_errors_short()):
                str_repr += f"Error {x + 1}:    " + error + "\n\n"
            str_repr += "\n\n"

        return str_repr

    def avg_dps(self, index):
        return round(sum([result.dps for result in self.results[index]]) / self.settings.sim_iterations, 2)

    def standard_deviation(self, index):
        avg_dps = self.avg_dps(index)
        sum_deviation = sum([(result.dps - avg_dps) ** 2 for result in self.results[index]])

        return round(sqrt(sum_deviation / len(self.results[index])), 2)

    def margin_of_error(self, index):
        # Z value for different confidence intervals
        z_value_95 = 1.960
        z_value_90 = 1.645
        return round(z_value_90 * (self.standard_deviation(index) / sqrt(len(self.results[index]))), 2)

    def write_result_files(self):
        file_path = self.settings.results_file_path
        if file_path is None:
            file_path = os.getcwd()

        if self.settings.full_log_for_best:
            with open(file_path + "Full_Combat_Log_Best_Sim_"
                      + self.start_time.strftime("%Y_%m_%d-%H_%M_%S") + ".log", "w") as file:
                file.write(max(self.results, key=lambda res: res.dps).full_combat_log)

        with open(file_path + "Complete_Sim_Result_"
                  + self.start_time.strftime("%Y_%m_%d-%H_%M_%S") + ".txt", "w") as file:
            file.write(str(self))
