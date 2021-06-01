from dataclasses import dataclass, field
from typing import Dict, Tuple

from PyQt5.QtCore import QObject, pyqtSignal

from src import enums
import src.db.sqlite_db_connector as DB
from src.gui.models.character_settings_model import CharacterSettingsModel


class SimSettingsModel(QObject):
    # Sim Settings
    sim_type_signal = pyqtSignal(str)
    sim_duration_signal = pyqtSignal(int)
    sim_iterations_signal = pyqtSignal(int)
    sim_combat_rater_signal = pyqtSignal(str)

    # Enemy Settings
    enemy_is_boss_signal = pyqtSignal(bool)
    enemy_level_signal = pyqtSignal(int)
    enemy_armor_signal = pyqtSignal(int)
    enemy_holy_res_signal = pyqtSignal(int)
    enemy_frost_res_signal = pyqtSignal(int)
    enemy_fire_res_signal = pyqtSignal(int)
    enemy_nature_res_signal = pyqtSignal(int)
    enemy_shadow_res_signal = pyqtSignal(int)
    enemy_arcane_res_signal = pyqtSignal(int)

    character_settings_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.sim_type = "dps"
        self.sim_duration = 300
        self.sim_iterations = 500
        self.sim_combat_rater = "FireMageCAR"

        self.enemy_is_boss = True
        self.enemy_level = 73
        self.enemy_armor = 0
        self.enemy_holy_res = 0
        self.enemy_frost_res = 0
        self.enemy_fire_res = 0
        self.enemy_nature_res = 0
        self.enemy_shadow_res = 0
        self.enemy_arcane_res = 0

        self.character_settings = []

    def set_default(self):
        self.sim_type = "dps"
        self.sim_duration = 300
        self.sim_iterations = 500
        self.sim_combat_rater = "FireMageCAR"

        self.enemy_is_boss = True
        self.enemy_level = 73
        self.enemy_armor = 0
        self.enemy_holy_res = 0
        self.enemy_frost_res = 0
        self.enemy_fire_res = 0
        self.enemy_nature_res = 0
        self.enemy_shadow_res = 0
        self.enemy_arcane_res = 0

        # if self.sim_type == "dps" and len(self.character_settings) != 1:
        #     self.character_settings = [CharacterSettingsModel()]
        # elif self.sim_type == "compare" and len(self.character_settings) != 2:
        #     self.character_settings = [CharacterSettingsModel(), CharacterSettingsModel()]
        self.set_character_settings()

    @property
    def character_settings(self):
        return self._character_settings

    @character_settings.setter
    def character_settings(self, value):
        self._character_settings = value
        self.character_settings_signal.emit(self._character_settings)

    def set_character_settings(self):
        if self.sim_type == "dps" and len(self.character_settings) != 1:
            if len(self.character_settings) == 0:
                self.character_settings = [CharacterSettingsModel()]
            else:
                self.character_settings = [self.character_settings[0]]

        elif self.sim_type == "compare" and len(self.character_settings) != 2:
            if len(self.character_settings) == 0:
                self.character_settings = [CharacterSettingsModel(), CharacterSettingsModel()]
            else:
                self.character_settings = [self.character_settings[0], CharacterSettingsModel()]

    @property
    def sim_type(self):
        return self._sim_type

    @sim_type.setter
    def sim_type(self, value):
        self._sim_type = value
        self.sim_type_signal.emit(self._sim_type)

    def set_sim_type(self, value):
        self._sim_type = value
        self.set_character_settings()

    @property
    def sim_duration(self):
        return self._sim_duration

    @sim_duration.setter
    def sim_duration(self, value):
        self._sim_duration = value
        self.sim_duration_signal.emit(self._sim_duration)

    def set_sim_duration(self, value):
        int_value = 0
        try:
            int_value = int(value)
        except ValueError:
            int_value = 0
        finally:
            self._sim_duration = int_value

    @property
    def sim_iterations(self):
        return self._sim_iterations

    @sim_iterations.setter
    def sim_iterations(self, value):
        self._sim_iterations = value
        self.sim_iterations_signal.emit(self._sim_iterations)

    def set_sim_iterations(self, value):
        int_value = 0
        try:
            int_value = int(value)
        except ValueError:
            int_value = 0
        finally:
            self._sim_iterations = int_value

    @property
    def sim_combat_rater(self):
        return self._sim_combat_rater

    @sim_combat_rater.setter
    def sim_combat_rater(self, value):
        self._sim_combat_rater = value
        self.sim_combat_rater_signal.emit(self._sim_combat_rater)

    def set_sim_combat_rater(self, value):
        self._sim_combat_rater = value

    @property
    def enemy_is_boss(self):
        return self._enemy_is_boss

    @enemy_is_boss.setter
    def enemy_is_boss(self, value):
        self._enemy_is_boss = value
        self.enemy_is_boss_signal.emit(self._enemy_is_boss)

    def set_enemy_is_boss(self, value):
        self._enemy_is_boss = value

    @property
    def enemy_level(self):
        return self._enemy_level

    @enemy_level.setter
    def enemy_level(self, value):
        self._enemy_level = value
        self.enemy_level_signal.emit(self._enemy_level)

    def set_enemy_level(self, value):
        self._enemy_level = value

    @property
    def enemy_armor(self):
        return self._enemy_armor

    @enemy_armor.setter
    def enemy_armor(self, value):
        self._enemy_armor = value
        self.enemy_armor_signal.emit(self._enemy_armor)

    def set_enemy_armor(self, value):
        self._enemy_armor = int(value)

    @property
    def enemy_holy_res(self):
        return self._enemy_holy_res

    @enemy_holy_res.setter
    def enemy_holy_res(self, value):
        self._enemy_holy_res = value
        self.enemy_holy_res_signal.emit(self._enemy_holy_res)

    def set_enemy_holy_res(self, value):
        self._enemy_holy_res = int(value)

    @property
    def enemy_frost_res(self):
        return self._enemy_frost_res

    @enemy_frost_res.setter
    def enemy_frost_res(self, value):
        self._enemy_frost_res = value
        self.enemy_frost_res_signal.emit(self._enemy_frost_res)

    def set_enemy_frost_res(self, value):
        self._enemy_frost_res = int(value)

    @property
    def enemy_fire_res(self):
        return self._enemy_fire_res

    @enemy_fire_res.setter
    def enemy_fire_res(self, value):
        self._enemy_fire_res = value
        self.enemy_fire_res_signal.emit(self._enemy_fire_res)

    def set_enemy_fire_res(self, value):
        self._enemy_fire_res = int(value)

    @property
    def enemy_nature_res(self):
        return self._enemy_nature_res

    @enemy_nature_res.setter
    def enemy_nature_res(self, value):
        self._enemy_nature_res = value
        self.enemy_nature_res_signal.emit(self._enemy_nature_res)

    def set_enemy_nature_res(self, value):
        self._enemy_nature_res = int(value)

    @property
    def enemy_shadow_res(self):
        return self._enemy_shadow_res

    @enemy_shadow_res.setter
    def enemy_shadow_res(self, value):
        self._enemy_shadow_res = value
        self.enemy_shadow_res_signal.emit(self._enemy_shadow_res)

    def set_enemy_shadow_res(self, value):
        self._enemy_shadow_res = int(value)

    @property
    def enemy_arcane_res(self):
        return self._enemy_arcane_res

    @enemy_arcane_res.setter
    def enemy_arcane_res(self, value):
        self._enemy_arcane_res = value
        self.enemy_arcane_res_signal.emit(self._enemy_arcane_res)

    def set_enemy_arcane_res(self, value):
        self._enemy_arcane_res = int(value)

    @property
    def sim_settings_dict(self):
        character_dict = {}
        for x, settings in enumerate(self.character_settings):
            character_dict[x] = settings.character_settings_dict

        sim_settings_dict = {"enemy": {"boss": self.enemy_is_boss,
                                       "level": self.enemy_level,
                                       "attributes": {"armor": self.enemy_armor,
                                                      "holy_resistance": self.enemy_holy_res,
                                                      "frost_resistance": self.enemy_frost_res,
                                                      "fire_resistance": self.enemy_fire_res,
                                                      "nature_resistance": self.enemy_nature_res,
                                                      "arcane_resistance": self.enemy_arcane_res,
                                                      "shadow_resistance": self.enemy_shadow_res}},
                             "simulation": {"sim_type": self.sim_type,
                                            "sim_duration": self.sim_duration,
                                            "sim_iterations": self.sim_iterations,
                                            "sim_combat_rater": self.sim_combat_rater,
                                            "full_log_for_best": True},
                             "character": character_dict}

        return sim_settings_dict

    def load_from_dict(self, settings_dict):

        if "enemy" in settings_dict:
            if "boss" in settings_dict["enemy"]:
                self.enemy_is_boss = settings_dict["enemy"]["boss"]

            if "level" in settings_dict["enemy"]:
                self.enemy_level = settings_dict["enemy"]["level"]

            if "attributes" in settings_dict["enemy"]:
                if "armor" in settings_dict["enemy"]["attributes"]:
                    self.enemy_armor = settings_dict["enemy"]["attributes"]["armor"]

                if "holy_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_holy_res = settings_dict["enemy"]["attributes"]["holy_resistance"]

                if "frost_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_frost_res = settings_dict["enemy"]["attributes"]["frost_resistance"]

                if "fire_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_fire_res = settings_dict["enemy"]["attributes"]["fire_resistance"]

                if "nature_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_nature_res = settings_dict["enemy"]["attributes"]["nature_resistance"]

                if "arcane_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_arcane_res = settings_dict["enemy"]["attributes"]["arcane_resistance"]

                if "shadow_resistance" in settings_dict["enemy"]["attributes"]:
                    self.enemy_shadow_res = settings_dict["enemy"]["attributes"]["shadow_resistance"]

        if "simulation" in settings_dict:
            if "sim_type" in settings_dict["simulation"]:
                self.sim_type = settings_dict["simulation"]["sim_type"]

            if "sim_duration" in settings_dict["simulation"]:
                self.sim_duration = settings_dict["simulation"]["sim_duration"]

            if "sim_iterations" in settings_dict["simulation"]:
                self.sim_iterations = settings_dict["simulation"]["sim_iterations"]

            if "sim_combat_rater" in settings_dict["simulation"]:
                self.sim_combat_rater = settings_dict["simulation"]["sim_combat_rater"]

        self.set_character_settings()
        if "character" in settings_dict:
            for index, character_settings_dict in enumerate(settings_dict["character"].values()):
                if index < len(self.character_settings):
                    self.character_settings[index].load_from_dict(character_settings_dict)
