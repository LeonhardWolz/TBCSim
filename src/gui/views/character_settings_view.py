from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIntValidator, QFontDatabase
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout, QComboBox, QLineEdit,
                             QCheckBox, QListWidget, QAbstractItemView, QLayout, QGridLayout)

import src.gui.views.gear_settings_view
from src.gui.widgets.line_dividers import QVLine, QHLine
from src.gui.widgets.select_from_list_dialog import QListWidgetItemID, SelectFromListDialog


class CharacterSettingsView(QWidget):
    def __init__(self, character_settings_model):
        super().__init__()
        self.character_settings_model = character_settings_model
        settings_hbox_layout = QHBoxLayout()
        settings_hbox_layout.setContentsMargins(11, 11, 0, 11)
        self.setLayout(settings_hbox_layout)

        settings_left_widget = QWidget()
        settings_left_widget.setMaximumWidth(530)

        character_settings_vbox_layout = QVBoxLayout()
        character_settings_vbox_layout.setContentsMargins(0, 0, 0, 0)

        character_settings_label = QLabel("Character Settings")
        character_settings_label.setStyleSheet("""font-size: 15pt;""")
        character_settings_label.setAlignment(Qt.AlignCenter)

        character_settings_vbox_layout.addWidget(character_settings_label)
        character_settings_vbox_layout.addWidget(QHLine())

        char_attributes_select_layout = QVBoxLayout()
        char_two_column_layout = QGridLayout()

        player_race_label = QLabel("<b>Race:</b>")
        player_race_label.setMinimumWidth(50)
        self.player_race_combo_box = QComboBox()
        self.player_race_combo_box.addItem("Troll")
        self.player_race_combo_box.addItem("Human")
        self.player_race_combo_box.addItem("Orc")
        self.player_race_combo_box.addItem("Dwarf")
        self.player_race_combo_box.addItem("Nightelf")
        self.player_race_combo_box.addItem("Tauren")
        self.player_race_combo_box.addItem("Gnome")
        self.player_race_combo_box.addItem("Bloodelf")
        self.player_race_combo_box.addItem("Draenei")

        char_two_column_layout.addWidget(player_race_label, 0, 0)
        char_two_column_layout.addWidget(self.player_race_combo_box, 0, 1)

        player_class_label = QLabel("<b>Class:</b>")
        player_class_label.setMinimumWidth(50)
        self.player_class_combo_box = QComboBox()
        self.player_class_combo_box.addItem("Mage")

        char_two_column_layout.addWidget(player_class_label, 1, 0)
        char_two_column_layout.addWidget(self.player_class_combo_box, 1, 1)

        talent_input_label = QLabel("<b>Talents:</b>")
        talent_input_label.setMinimumWidth(50)
        talent_input_label.setToolTip("Paste a link from the \"tbc.wowhead.com/talent-calc\" "
                                      "talent calculator into this field.")
        self.player_talents_line_edit = QLineEdit()

        char_two_column_layout.addWidget(talent_input_label, 2, 0)
        char_two_column_layout.addWidget(self.player_talents_line_edit, 2, 1)

        ch_active_spells = QHBoxLayout()

        active_spells_label = QLabel("<b>Active<br>Spells:</b>")
        active_spells_label.setToolTip("Damage spells that are considered for use during the Simulation.\n"
                                       "Power-up spells like Arcane Power don't belong here. "
                                       "Those will get used automatically.")
        active_spells_label.setFixedWidth(85)
        active_spells_label.setAlignment(Qt.AlignTop)

        self.active_spells_list = QListWidget()
        self.active_spells_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.active_spells_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.active_spells_list.setMinimumHeight(50)
        self.active_spells_list.setMaximumHeight(200)
        self.active_spells_list.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        active_spells_buttons = QVBoxLayout()

        self.active_spells_add_button = QPushButton("Add")
        self.active_spells_add_button.setFixedWidth(50)

        self.active_spells_remove_button = QPushButton("Remove")
        self.active_spells_remove_button.setFixedWidth(50)

        active_spells_buttons.addWidget(self.active_spells_add_button)
        active_spells_buttons.addWidget(self.active_spells_remove_button)

        ch_active_spells.addWidget(active_spells_label)
        ch_active_spells.addWidget(self.active_spells_list)
        ch_active_spells.addLayout(active_spells_buttons)

        ch_passive_spells = QHBoxLayout()

        passive_spells_label = QLabel("<b>Passive<br>Spells:</b>")
        passive_spells_label.setToolTip("Spells that are applied automatically at the beginning of the simulation\n"
                                        "such as Power Word: Fortitude or Arcane Intellect.")
        passive_spells_label.setFixedWidth(85)
        passive_spells_label.setAlignment(Qt.AlignTop)

        self.passive_spells_list = QListWidget()
        self.passive_spells_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.passive_spells_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.passive_spells_list.setMinimumHeight(50)
        self.passive_spells_list.setMaximumHeight(200)
        self.passive_spells_list.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        passive_spells_buttons = QVBoxLayout()

        self.passive_spells_add_button = QPushButton("Add")
        self.passive_spells_add_button.setFixedWidth(50)

        self.passive_spells_remove_button = QPushButton("Remove")
        self.passive_spells_remove_button.setFixedWidth(50)

        passive_spells_buttons.addWidget(self.passive_spells_add_button)
        passive_spells_buttons.addWidget(self.passive_spells_remove_button)

        ch_passive_spells.addWidget(passive_spells_label)
        ch_passive_spells.addWidget(self.passive_spells_list)
        ch_passive_spells.addLayout(passive_spells_buttons)

        ch_active_consumables = QHBoxLayout()

        active_consumables_label = QLabel("<b>Active<br>Consumables:</b>")
        active_consumables_label.setToolTip("Consumables that are to be used during the simulation\n"
                                            "such as Mana Potions or Combat Potions.")
        active_consumables_label.setFixedWidth(85)
        active_consumables_label.setAlignment(Qt.AlignTop)

        self.active_consumables_list = QListWidget()
        self.active_consumables_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.active_consumables_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.active_consumables_list.setMinimumHeight(50)
        self.active_consumables_list.setMaximumHeight(200)
        self.active_consumables_list.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        active_consumables_buttons = QVBoxLayout()

        self.active_consumables_add_button = QPushButton("Add")
        self.active_consumables_add_button.setFixedWidth(50)

        self.active_consumables_remove_button = QPushButton("Remove")
        self.active_consumables_remove_button.setFixedWidth(50)

        active_consumables_buttons.addWidget(self.active_consumables_add_button)
        active_consumables_buttons.addWidget(self.active_consumables_remove_button)

        ch_active_consumables.addWidget(active_consumables_label)
        ch_active_consumables.addWidget(self.active_consumables_list)
        ch_active_consumables.addLayout(active_consumables_buttons)

        ch_passive_consumables = QHBoxLayout()

        passive_consumables_label = QLabel("<b>Passive<br>Consumables:</b>")
        passive_consumables_label.setToolTip("Consumables that are already applied when the simulation begins\n"
                                             "such as Flasks or Bufffood.")
        passive_consumables_label.setFixedWidth(85)
        passive_consumables_label.setAlignment(Qt.AlignTop)

        self.passive_consumables_list = QListWidget()
        self.passive_consumables_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.passive_consumables_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.passive_consumables_list.setMinimumHeight(50)
        self.passive_consumables_list.setMaximumHeight(200)
        self.passive_consumables_list.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        passive_consumables_buttons = QVBoxLayout()

        self.passive_consumables_add_button = QPushButton("Add")
        self.passive_consumables_add_button.setFixedWidth(50)

        self.passive_consumables_remove_button = QPushButton("Remove")
        self.passive_consumables_remove_button.setFixedWidth(50)

        passive_consumables_buttons.addWidget(self.passive_consumables_add_button)
        passive_consumables_buttons.addWidget(self.passive_consumables_remove_button)

        ch_passive_consumables.addWidget(passive_consumables_label)
        ch_passive_consumables.addWidget(self.passive_consumables_list)
        ch_passive_consumables.addLayout(passive_consumables_buttons)

        char_attributes_select_layout.addLayout(char_two_column_layout)
        char_attributes_select_layout.addLayout(ch_active_spells)
        char_attributes_select_layout.addLayout(ch_passive_spells)
        char_attributes_select_layout.addLayout(ch_active_consumables)
        char_attributes_select_layout.addLayout(ch_passive_consumables)

        character_settings_vbox_layout.addLayout(char_attributes_select_layout)

        settings_left_widget.setLayout(character_settings_vbox_layout)

        ch_gear_widget = src.gui.views.gear_settings_view.GearView(self.character_settings_model)

        settings_hbox_layout.addWidget(settings_left_widget)
        settings_hbox_layout.addSpacing(10)
        settings_hbox_layout.addWidget(QVLine())
        settings_hbox_layout.addSpacing(10)
        settings_hbox_layout.addWidget(ch_gear_widget)

        # Dialog boxes
        self.active_spells_add_dialog = SelectFromListDialog(self.character_settings_model.add_active_spell)
        self.active_spells_add_dialog.setWindowTitle("Add Active Spell")
        self.active_spells_add_dialog.set_dict_signal(self.character_settings_model.spell_dict_signal)

        self.passive_spells_add_dialog = SelectFromListDialog(self.character_settings_model.add_passive_spell)
        self.passive_spells_add_dialog.setWindowTitle("Add Passive Spell")
        self.passive_spells_add_dialog.set_dict_signal(self.character_settings_model.spell_dict_signal)

        self.passive_consumables_add_dialog = SelectFromListDialog(self.character_settings_model.add_passive_consumable)
        self.passive_consumables_add_dialog.setWindowTitle("Add Passive Consumable")
        self.passive_consumables_add_dialog.set_dict_signal(self.character_settings_model.consumable_dict_signal)

        self.active_consumables_add_dialog = SelectFromListDialog(self.character_settings_model.add_active_consumable)
        self.active_consumables_add_dialog.setWindowTitle("Add Active Consumable")
        self.active_consumables_add_dialog.set_dict_signal(self.character_settings_model.consumable_dict_signal)

        self._connect_signals()

        self.character_settings_model.set_default()

    def _connect_signals(self):

        self.character_settings_model.player_race_signal.connect(self.player_race)
        self.player_race_combo_box.activated.connect(lambda:
                                                     self.character_settings_model.set_player_race(
                                                         self.player_race_combo_box.currentText()))

        self.character_settings_model.player_class_signal.connect(self.player_class)
        self.player_class_combo_box.activated.connect(lambda:
                                                      self.character_settings_model.set_player_class(
                                                          self.player_class_combo_box.currentText()))

        self.character_settings_model.player_talents_string_signal.connect(self.player_talents)
        self.player_talents_line_edit.textChanged.connect(self.character_settings_model.set_player_talents_string)

        self.active_spells_add_button.clicked.connect(self.active_spells_add_dialog.exec_)
        self.active_spells_remove_button.clicked.connect(self.remove_active_spell)
        self.character_settings_model.active_spells_signal.connect(self.active_spells)

        self.passive_spells_add_button.clicked.connect(self.passive_spells_add_dialog.exec_)
        self.passive_spells_remove_button.clicked.connect(self.remove_passive_spell)
        self.character_settings_model.passive_spells_signal.connect(self.passive_spells)

        self.passive_consumables_add_button.clicked.connect(self.passive_consumables_add_dialog.exec_)
        self.passive_consumables_remove_button.clicked.connect(self.remove_passive_consumables)
        self.character_settings_model.passive_consumables_signal.connect(self.passive_consumables)

        self.active_consumables_add_button.clicked.connect(self.active_consumables_add_dialog.exec_)
        self.active_consumables_remove_button.clicked.connect(self.remove_active_consumable)
        self.character_settings_model.active_consumables_signal.connect(self.active_consumables)

    def remove_active_spell(self):
        for item in self.active_spells_list.selectedItems():
            self.character_settings_model.remove_active_spell(item.object_id)

    def remove_passive_spell(self):
        for item in self.passive_spells_list.selectedItems():
            self.character_settings_model.remove_passive_spell(item.object_id)

    def remove_passive_consumables(self):
        for item in self.passive_consumables_list.selectedItems():
            self.character_settings_model.remove_passive_consumable(item.object_id)

    def remove_active_consumable(self):
        for item in self.active_consumables_list.selectedItems():
            self.character_settings_model.remove_active_consumable(item.object_id)

    @pyqtSlot(str)
    def player_race(self, value):
        self.player_race_combo_box.setCurrentIndex(self.player_race_combo_box.findText(str(value)))

    @pyqtSlot(str)
    def player_class(self, value):
        self.player_class_combo_box.setCurrentIndex(self.player_class_combo_box.findText(str(value)))

    @pyqtSlot(str)
    def player_talents(self, value):
        self.player_talents_line_edit.setText(value)

    @pyqtSlot(dict)
    def active_spells(self, dictionary):
        self.set_list_widget_with_dict(dictionary, self.active_spells_list)

    @pyqtSlot(dict)
    def passive_spells(self, dictionary):
        self.set_list_widget_with_dict(dictionary, self.passive_spells_list)

    @pyqtSlot(dict)
    def passive_consumables(self, dictionary):
        self.set_list_widget_with_dict(dictionary, self.passive_consumables_list)

    @pyqtSlot(dict)
    def active_consumables(self, dictionary):
        self.set_list_widget_with_dict(dictionary, self.active_consumables_list)

    def set_list_widget_with_dict(self, dictionary, list_widget):
        current_keys = []
        for item in self.get_list_items(list_widget):
            if item.object_id not in dictionary.keys():
                list_widget.takeItem(list_widget.row(item))
            else:
                current_keys.append(item.object_id)

        for key, spell in [(spell_key, dictionary[spell_key][0])
                           for spell_key in dictionary.keys() if spell_key not in current_keys]:
            QListWidgetItemID("{:7s}{}".format(str(key), spell), list_widget, key)

    @staticmethod
    def get_list_items(list_widget):
        items = []
        for x in range(list_widget.count()):
            items.append(list_widget.item(x))
        return items
