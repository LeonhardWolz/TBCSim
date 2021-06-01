from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QComboBox, QLineEdit,
                             QCheckBox, QGridLayout)

from src.gui.widgets.line_dividers import QVLine, QHLine
from src.gui.widgets.select_from_list_dialog import QListWidgetItemID


class SimSettingsView(QWidget):
    def __init__(self, settings_model):
        super().__init__()
        self.settings_model = settings_model

        settings_top_hbox_layout = QHBoxLayout()
        self.setLayout(settings_top_hbox_layout)

        sim_settings_vbox_layout = QVBoxLayout()

        sim_settings_label = QLabel("Simulation Settings")
        sim_settings_label.setStyleSheet("""font-size: 15pt;""")
        sim_settings_label.setAlignment(Qt.AlignCenter)

        sim_settings_vbox_layout.addWidget(sim_settings_label)
        sim_settings_vbox_layout.addWidget(QHLine())

        sim_settings_grid_layout = QGridLayout()

        sim_type_label = QLabel("<b>Sim. Type:</b>")
        sim_type_label.setMinimumWidth(120)
        self.sim_type_combo_box = QComboBox()
        self.sim_type_combo_box.addItem("dps")
        self.sim_type_combo_box.addItem("compare")

        sim_settings_grid_layout.addWidget(sim_type_label, 0, 0)
        sim_settings_grid_layout.addWidget(self.sim_type_combo_box, 0, 1)

        sim_duration_label = QLabel("<b>Sim. Duration:</b>")
        sim_duration_label.setMinimumWidth(120)
        self.sim_duration_entry = QLineEdit()
        self.sim_duration_entry.setValidator(QIntValidator())

        sim_settings_grid_layout.addWidget(sim_duration_label, 1, 0)
        sim_settings_grid_layout.addWidget(self.sim_duration_entry, 1, 1)

        sim_iterations_label = QLabel("<b>Sim. Iterations:</b>")
        sim_iterations_label.setMinimumWidth(120)
        sim_iterations_label.setToolTip("For best results use a value of at least 200 or above.")
        self.sim_iterations_entry = QLineEdit()
        self.sim_iterations_entry.setValidator(QIntValidator())

        sim_settings_grid_layout.addWidget(sim_iterations_label, 2, 0)
        sim_settings_grid_layout.addWidget(self.sim_iterations_entry, 2, 1)

        sim_rater_label = QLabel("<b>Sim. Combat Rater:</b>")
        sim_rater_label.setMinimumWidth(120)
        sim_rater_label.setToolTip("The combat rater evaluates possible combat actions.<br>"
                                   "The rating system is different for different specs.")
        self.sim_rater_combo_box = QComboBox()
        self.sim_rater_combo_box.addItem("FireMageCAR")
        self.sim_rater_combo_box.addItem("ArcaneMageCAR")

        sim_settings_grid_layout.addWidget(sim_rater_label, 3, 0)
        sim_settings_grid_layout.addWidget(self.sim_rater_combo_box, 3, 1)

        sim_settings_vbox_layout.addLayout(sim_settings_grid_layout)
        sim_settings_vbox_layout.setAlignment(Qt.AlignTop)

        enemy_settings_vbox_layout = QVBoxLayout()

        enemy_settings_label = QLabel("Enemy Settings")
        enemy_settings_label.setStyleSheet("""font-size: 15pt;""")
        enemy_settings_label.setAlignment(Qt.AlignCenter)

        enemy_settings_vbox_layout.addWidget(enemy_settings_label)
        enemy_settings_vbox_layout.addWidget(QHLine())

        enemy_settings_form_layout = QFormLayout()

        self.enemy_is_boss_check_box = QCheckBox()
        enemy_settings_form_layout.addRow("<b>Boss:</b>", self.enemy_is_boss_check_box)

        self.enemy_level_combo_box = QComboBox()
        self.enemy_level_combo_box.addItem("70")
        self.enemy_level_combo_box.addItem("71")
        self.enemy_level_combo_box.addItem("72")
        self.enemy_level_combo_box.addItem("73")
        self.enemy_level_combo_box.setCurrentIndex(3)
        enemy_settings_form_layout.addRow("<b>Enemy Level:</b>", self.enemy_level_combo_box)

        self.enemy_armor_entry = QLineEdit()
        self.enemy_armor_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Armor:</b>", self.enemy_armor_entry)

        self.enemy_holy_resistance_entry = QLineEdit()
        self.enemy_holy_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Holy Res.:</b>", self.enemy_holy_resistance_entry)

        self.enemy_frost_resistance_entry = QLineEdit()
        self.enemy_frost_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Frost Res.:</b>", self.enemy_frost_resistance_entry)

        self.enemy_fire_resistance_entry = QLineEdit()
        self.enemy_fire_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Fire Res.:</b>", self.enemy_fire_resistance_entry)

        self.enemy_nature_resistance_entry = QLineEdit()
        self.enemy_nature_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Nature Res.:</b>", self.enemy_nature_resistance_entry)

        self.enemy_shadow_resistance_entry = QLineEdit()
        self.enemy_shadow_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Shadow Res.:</b>", self.enemy_shadow_resistance_entry)

        self.enemy_arcane_resistance_entry = QLineEdit()
        self.enemy_arcane_resistance_entry.setValidator(QIntValidator())
        enemy_settings_form_layout.addRow("<b>Enemy Arcane Res.:</b>", self.enemy_arcane_resistance_entry)

        enemy_settings_vbox_layout.addLayout(enemy_settings_form_layout)
        enemy_settings_vbox_layout.setAlignment(Qt.AlignTop)

        settings_top_hbox_layout.addLayout(sim_settings_vbox_layout)
        settings_top_hbox_layout.addWidget(QVLine())
        settings_top_hbox_layout.addLayout(enemy_settings_vbox_layout)

        self._connect_signals()

        #self.settings_model.set_default()

    def _connect_signals(self):
        self.settings_model.sim_type_signal.connect(self.sim_type)
        self.sim_type_combo_box.activated.connect(lambda:
                                                  self.settings_model.set_sim_type(
                                                      self.sim_type_combo_box.currentText()))

        self.settings_model.sim_duration_signal.connect(self.sim_duration)
        self.sim_duration_entry.textChanged.connect(self.settings_model.set_sim_duration)

        self.settings_model.sim_iterations_signal.connect(self.sim_iterations)
        self.sim_iterations_entry.textChanged.connect(self.settings_model.set_sim_iterations)

        self.settings_model.sim_combat_rater_signal.connect(self.sim_combat_rater)
        self.sim_rater_combo_box.activated.connect(lambda:
                                                   self.settings_model.set_sim_combat_rater(
                                                       self.sim_rater_combo_box.currentText()))

        self.settings_model.enemy_is_boss_signal.connect(self.enemy_is_boss)
        self.enemy_is_boss_check_box.clicked.connect(lambda:
                                                     self.settings_model.set_enemy_is_boss(
                                                         self.enemy_is_boss_check_box.isChecked()))

        self.settings_model.enemy_level_signal.connect(self.enemy_level)
        self.enemy_level_combo_box.activated.connect(lambda:
                                                     self.settings_model.set_enemy_level(
                                                         self.enemy_level_combo_box.currentText()))

        self.settings_model.enemy_armor_signal.connect(self.enemy_armor)
        self.enemy_armor_entry.textChanged.connect(self.settings_model.set_enemy_armor)

        self.settings_model.enemy_holy_res_signal.connect(self.enemy_holy_res)
        self.enemy_holy_resistance_entry.textChanged.connect(self.settings_model.set_enemy_holy_res)

        self.settings_model.enemy_frost_res_signal.connect(self.enemy_frost_res)
        self.enemy_frost_resistance_entry.textChanged.connect(self.settings_model.set_enemy_frost_res)

        self.settings_model.enemy_fire_res_signal.connect(self.enemy_fire_res)
        self.enemy_fire_resistance_entry.textChanged.connect(self.settings_model.set_enemy_fire_res)

        self.settings_model.enemy_nature_res_signal.connect(self.enemy_nature_res)
        self.enemy_nature_resistance_entry.textChanged.connect(self.settings_model.set_enemy_nature_res)

        self.settings_model.enemy_shadow_res_signal.connect(self.enemy_shadow_res)
        self.enemy_shadow_resistance_entry.textChanged.connect(self.settings_model.set_enemy_shadow_res)

        self.settings_model.enemy_arcane_res_signal.connect(self.enemy_arcane_res)
        self.enemy_arcane_resistance_entry.textChanged.connect(self.settings_model.set_enemy_arcane_res)

    @pyqtSlot(str)
    def sim_type(self, value):
        self.sim_type_combo_box.setCurrentIndex(self.sim_type_combo_box.findText(value))

    @pyqtSlot(int)
    def sim_duration(self, value):
        self.sim_duration_entry.setText(str(value))

    @pyqtSlot(int)
    def sim_iterations(self, value):
        self.sim_iterations_entry.setText(str(value))

    @pyqtSlot(str)
    def sim_combat_rater(self, value):
        self.sim_rater_combo_box.setCurrentIndex(self.sim_rater_combo_box.findText(value))

    @pyqtSlot(bool)
    def enemy_is_boss(self, value):
        self.enemy_is_boss_check_box.setChecked(value)

    @pyqtSlot(int)
    def enemy_level(self, value):
        self.enemy_level_combo_box.setCurrentIndex(self.enemy_level_combo_box.findText(str(value)))

    @pyqtSlot(int)
    def enemy_armor(self, value):
        self.enemy_armor_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_holy_res(self, value):
        self.enemy_holy_resistance_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_frost_res(self, value):
        self.enemy_frost_resistance_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_fire_res(self, value):
        self.enemy_fire_resistance_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_nature_res(self, value):
        self.enemy_nature_resistance_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_shadow_res(self, value):
        self.enemy_shadow_resistance_entry.setText(str(value))

    @pyqtSlot(int)
    def enemy_arcane_res(self, value):
        self.enemy_arcane_resistance_entry.setText(str(value))

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
