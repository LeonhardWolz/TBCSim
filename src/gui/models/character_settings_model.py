from dataclasses import dataclass, field
from typing import Dict, Tuple

from PyQt5.QtCore import QObject, pyqtSignal

from src import enums
import src.db.sqlite_db_connector as DB


class CharacterSettingsModel(QObject):
    # Character Settings
    player_race_signal = pyqtSignal(str)
    player_class_signal = pyqtSignal(str)
    player_talents_string_signal = pyqtSignal(str)
    active_spells_signal = pyqtSignal(dict)
    passive_spells_signal = pyqtSignal(dict)
    passive_consumables_signal = pyqtSignal(dict)
    active_consumables_signal = pyqtSignal(dict)

    # gear
    equipped_gear_signal = pyqtSignal(dict)

    # all spells and items
    spell_dict_signal = pyqtSignal(dict)
    consumable_dict_signal = pyqtSignal(dict)
    gem_dict_signal = pyqtSignal(dict)
    enchantment_dict_signal = pyqtSignal(dict)

    # signal for different gear slots
    ammo_gear_dict_signal = pyqtSignal(dict)
    head_gear_dict_signal = pyqtSignal(dict)
    neck_gear_dict_signal = pyqtSignal(dict)
    shoulder_gear_dict_signal = pyqtSignal(dict)
    body_gear_dict_signal = pyqtSignal(dict)
    chest_gear_dict_signal = pyqtSignal(dict)
    waist_gear_dict_signal = pyqtSignal(dict)
    legs_gear_dict_signal = pyqtSignal(dict)
    feet_gear_dict_signal = pyqtSignal(dict)
    wrist_gear_dict_signal = pyqtSignal(dict)
    hand_gear_dict_signal = pyqtSignal(dict)
    finger_gear_dict_signal = pyqtSignal(dict)
    trinket_gear_dict_signal = pyqtSignal(dict)
    back_gear_dict_signal = pyqtSignal(dict)
    mainhand_gear_dict_signal = pyqtSignal(dict)
    offhand_gear_dict_signal = pyqtSignal(dict)
    ranged_gear_dict_signal = pyqtSignal(dict)
    tabard_gear_dict_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.player_race = "Troll"
        self.player_class = "Mage"
        self.player_talents_string = ""
        self.active_spells = {}
        self.passive_spells = {}
        self.passive_consumables = {}
        self.active_consumables = {}

        temp_gear_dict = {}
        for inventory_slot in enums.inventory_slot.items():
            temp_gear_dict[inventory_slot[0]] = EquippedItem()
        self.equipped_gear = temp_gear_dict

        self.spell_dict = {}
        self.consumable_dict = {}
        self.gem_dict = {}
        self.enchantment_dict = {}

        self.edit_gear_dict = {}
        self.edit_gear_signals = {0: self.ammo_gear_dict_signal,
                                  1: self.head_gear_dict_signal,
                                  2: self.neck_gear_dict_signal,
                                  3: self.shoulder_gear_dict_signal,
                                  4: self.body_gear_dict_signal,
                                  5: self.chest_gear_dict_signal,
                                  6: self.waist_gear_dict_signal,
                                  7: self.legs_gear_dict_signal,
                                  8: self.feet_gear_dict_signal,
                                  9: self.wrist_gear_dict_signal,
                                  10: self.hand_gear_dict_signal,
                                  11: self.finger_gear_dict_signal,
                                  12: self.finger_gear_dict_signal,
                                  13: self.trinket_gear_dict_signal,
                                  14: self.trinket_gear_dict_signal,
                                  15: self.back_gear_dict_signal,
                                  16: self.mainhand_gear_dict_signal,
                                  17: self.offhand_gear_dict_signal,
                                  18: self.ranged_gear_dict_signal,
                                  19: self.tabard_gear_dict_signal}

    def set_default(self):
        self.player_race = "Troll"
        self.player_class = "Mage"
        self.player_talents_string = ""
        self.active_spells = {}
        self.passive_spells = {}
        self.passive_consumables = {}
        self.active_consumables = {}

        temp_gear_dict = {}
        for inventory_slot in enums.inventory_slot.items():
            temp_gear_dict[inventory_slot[0]] = EquippedItem()
        self.equipped_gear = temp_gear_dict

        self.spell_dict = DB.get_gui_spell_dict()
        self.consumable_dict = DB.get_gui_consumable_dict()
        self.gem_dict = DB.get_gui_gem_dict()
        self.enchantment_dict = {}

    @property
    def player_race(self):
        return self._player_race

    @player_race.setter
    def player_race(self, value):
        self._player_race = value
        self.player_race_signal.emit(self._player_race)

    def set_player_race(self, value):
        self._player_race = value

    @property
    def player_class(self):
        return self._player_class

    @player_class.setter
    def player_class(self, value):
        self._player_class = value
        self.player_class_signal.emit(self._player_class)

    def set_player_class(self, value):
        self._player_class = value

    @property
    def player_talents_string(self):
        return self._player_talents_string

    @player_talents_string.setter
    def player_talents_string(self, value):
        self._player_talents_string = value
        self.player_talents_string_signal.emit(self._player_talents_string)

    def set_player_talents_string(self, value):
        self._player_talents_string = str(value)

    @property
    def active_spells(self):
        return self._active_spells

    @active_spells.setter
    def active_spells(self, value):
        self._active_spells = value
        self.active_spells_signal.emit(self._active_spells)

    def add_active_spell(self, spell_id):
        self.active_spells[spell_id] = self.spell_dict[spell_id]
        self.active_spells_signal.emit(self._active_spells)

    def remove_active_spell(self, spell_id):
        del self.active_spells[spell_id]
        self.active_spells_signal.emit(self._active_spells)

    @property
    def passive_spells(self):
        return self._passive_spells

    @passive_spells.setter
    def passive_spells(self, value):
        self._passive_spells = value
        self.passive_spells_signal.emit(self._passive_spells)

    def add_passive_spell(self, spell_id):
        self.passive_spells[spell_id] = self.spell_dict[spell_id]
        self.passive_spells_signal.emit(self._passive_spells)

    def remove_passive_spell(self, spell_id):
        del self.passive_spells[spell_id]
        self.passive_spells_signal.emit(self._passive_spells)

    @property
    def passive_consumables(self):
        return self._passive_consumables

    @passive_consumables.setter
    def passive_consumables(self, value):
        self._passive_consumables = value
        self.passive_consumables_signal.emit(self._passive_consumables)

    def add_passive_consumable(self, consumable_id):
        self.passive_consumables[consumable_id] = self.consumable_dict[consumable_id]
        self.passive_consumables_signal.emit(self._passive_consumables)

    def remove_passive_consumable(self, consumable_id):
        del self.passive_consumables[consumable_id]
        self.passive_consumables_signal.emit(self._passive_consumables)

    @property
    def active_consumables(self):
        return self._active_consumables

    @active_consumables.setter
    def active_consumables(self, value):
        self._active_consumables = value
        self.active_consumables_signal.emit(self._active_consumables)

    def add_active_consumable(self, consumable_id):
        self.active_consumables[consumable_id] = self.consumable_dict[consumable_id]
        self.active_consumables_signal.emit(self._active_consumables)

    def remove_active_consumable(self, consumable_id):
        del self.active_consumables[consumable_id]
        self.active_consumables_signal.emit(self._active_consumables)

    @property
    def spell_dict(self):
        return self._spell_dict

    @spell_dict.setter
    def spell_dict(self, value):
        self._spell_dict = value
        self.spell_dict_signal.emit(self._spell_dict)

    @property
    def consumable_dict(self):
        return self._consumable_dict

    @consumable_dict.setter
    def consumable_dict(self, value):
        self._consumable_dict = value
        self.consumable_dict_signal.emit(self._consumable_dict)

    @property
    def gem_dict(self):
        return self._gem_dict

    @gem_dict.setter
    def gem_dict(self, value):
        self._gem_dict = value
        self.gem_dict_signal.emit(self._gem_dict)

    @property
    def enchantment_dict(self):
        return self._enchantment_dict

    @enchantment_dict.setter
    def enchantment_dict(self, value):
        self._enchantment_dict = value
        self.enchantment_dict_signal.emit(self._enchantment_dict)

    def set_ench_dict(self, inv_slot):
        item = DB.get_item(self._equipped_gear[inv_slot].item_id)
        item_class = item[DB.item_column_info["class"]]

        if item_class == 4:
            type_mask = 0
            for inv_type in enums.inv_type_in_slot[inv_slot]:
                type_mask |= 1 << inv_type
            self.enchantment_dict = DB.get_gui_enchantments_dict(item_class=item_class,
                                                                 inventory_type_mask=type_mask)
        elif item_class == 2:
            subclass_mask = 1 << item[DB.item_column_info["subclass"]]
            self.enchantment_dict = DB.get_gui_enchantments_dict(item_class=item_class,
                                                                 item_subclass_mask=subclass_mask)

    def emit_edit_gear_dict_slot(self, inv_slot):
        if inv_slot not in self.edit_gear_dict:
            self.edit_gear_dict[inv_slot] = DB.get_gear_items_for_slot(inv_slot)
        self.edit_gear_signals[inv_slot].emit(self.edit_gear_dict[inv_slot])

    @property
    def equipped_gear(self):
        return self._equipped_gear

    @equipped_gear.setter
    def equipped_gear(self, value):
        self._equipped_gear = value
        self.equipped_gear_signal.emit(self._equipped_gear)

    def set_gear_slot(self, inv_slot, item_id):
        if item_id == 0:
            self._equipped_gear[inv_slot] = EquippedItem()
        else:
            item_from_db = DB.get_item(item_id)
            self._equipped_gear[inv_slot].item_id = item_id
            self._equipped_gear[inv_slot].name = item_from_db[DB.item_column_info["name"]]
            self._equipped_gear[inv_slot].can_enchant = \
                DB.get_item_can_be_enchanted(item_from_db[DB.item_column_info["class"]],
                                             1 << item_from_db[DB.item_column_info["subclass"]],
                                             1 << item_from_db[
                                                 DB.item_column_info["InventoryType"]])

            self._equipped_gear[inv_slot].enchantment = None
            self._equipped_gear[inv_slot].sockets = {}

            for i in range(1, 4):
                socket_color = item_from_db[DB.item_column_info["socketColor_" + str(i)]]
                if socket_color:
                    self.add_gear_socket(inv_slot, i - 1, socket_color)
        self.equipped_gear_signal.emit(self._equipped_gear)

    def get_equipped_gear_as_dict_for_yaml(self):
        dict_for_yaml = {}
        for equipped_item in self.equipped_gear.items():
            if equipped_item[1].item_id:
                inv_slot = {"item_id": equipped_item[1].item_id}
                if equipped_item[1].enchantment:
                    inv_slot["enchant"] = equipped_item[1].enchantment[0]

                if equipped_item[1].sockets:
                    for x, gem_slot in enumerate(equipped_item[1].sockets.values()):
                        if gem_slot["socket_content_id"] is not None:
                            if "gems" not in inv_slot:
                                inv_slot["gems"] = {}
                            inv_slot["gems"][x + 1] = gem_slot["socket_content_id"]

                dict_for_yaml[equipped_item[0]] = inv_slot

        return dict_for_yaml

    def set_gear_enchantment(self, inv_slot, enchantment_id):
        self._equipped_gear[inv_slot].enchantment = enchantment_id if not enchantment_id else \
            (enchantment_id, DB.get_enchant_name(enchantment_id))
        self.equipped_gear_signal.emit(self._equipped_gear)

    def remove_gear_enchantment(self, inv_slot):
        self._equipped_gear[inv_slot].enchantment = None
        self.equipped_gear_signal.emit(self._equipped_gear)

    def add_gear_socket(self, inv_slot, socket_slot, socket_color, socket_content=None):
        self._equipped_gear[inv_slot].sockets[socket_slot] = {"socket_color_mask": socket_color,
                                                              "socket_color_name":
                                                                  enums.socket_color_name[socket_color],
                                                              "socket_content_id": socket_content,
                                                              "socket_content_name":
                                                                  DB.get_item_name(socket_content)
                                                                  if socket_content else None}

    def set_socket_gem(self, inv_slot, socket_slot, socket_content):
        self._equipped_gear[inv_slot].sockets[socket_slot]["socket_content_id"] = socket_content \
            if socket_content else None
        self._equipped_gear[inv_slot].sockets[socket_slot]["socket_content_name"] = \
            DB.get_item_name(socket_content) if socket_content else None

        self.equipped_gear_signal.emit(self._equipped_gear)

    @property
    def character_settings_dict(self):
        character_settings_dict = {"race": self.player_race,
                                   "class": self.player_class,
                                   "active_spells": list(self.active_spells.keys()),
                                   "passive_spells": list(self.passive_spells.keys()),
                                   "passive_consumables": list(self.passive_consumables.keys()),
                                   "active_consumables": list(self.active_consumables.keys()),
                                   "gear": self.get_equipped_gear_as_dict_for_yaml(),
                                   "talent_calc_link": str(self.player_talents_string)}

        return character_settings_dict

    def load_from_dict(self, character_settings_dict):
        if "race" in character_settings_dict:
            self.player_race = character_settings_dict["race"]

        if "class" in character_settings_dict:
            self.player_class = character_settings_dict["class"]

        if "active_spells" in character_settings_dict:
            self.active_spells = {}
            for spell in character_settings_dict["active_spells"]:
                self.add_active_spell(spell)

        if "passive_spells" in character_settings_dict:
            self.passive_spells = {}
            for spell in character_settings_dict["passive_spells"]:
                self.add_passive_spell(spell)

        if "active_consumables" in character_settings_dict:
            self.active_consumables = {}
            for consumable in character_settings_dict["active_consumables"]:
                self.add_active_consumable(consumable)

        if "passive_consumables" in character_settings_dict:
            self.passive_consumables = {}
            for consumable in character_settings_dict["passive_consumables"]:
                self.add_passive_consumable(consumable)

        if "gear" in character_settings_dict:
            for item in character_settings_dict["gear"].items():
                if item[1] is not None:
                    self.set_gear_slot(item[0], item[1]["item_id"])

                    if "enchant" in item[1]:
                        self.set_gear_enchantment(item[0], item[1]["enchant"])

                    if "gems" in item[1]:
                        for socket in item[1]["gems"].items():
                            self.set_socket_gem(item[0], socket[0] - 1, socket[1])

        if "talent_calc_link" in character_settings_dict:
            self.player_talents_string = character_settings_dict["talent_calc_link"]


@dataclass
class EquippedItem:
    item_id: int = None
    name: str = None
    can_enchant: bool = True
    enchantment: Tuple = field(default_factory=lambda: ())
    sockets: Dict = field(default_factory=lambda: {})
