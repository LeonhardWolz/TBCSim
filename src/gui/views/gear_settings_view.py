from functools import partial

from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QSizePolicy,
                             QLayout)

from src import enums
from src.gui.widgets.line_dividers import QVLine, QHLine
from src.gui.widgets.select_from_list_dialog import SelectFromListDialog


class GearView(QWidget):
    def __init__(self, settings_model):
        super().__init__()
        self.settings_model = settings_model
        self.gear_slots = {}
        self.gear_slot_buttons = {}
        self.gear_slot_edit_dialog = {}

        ch_settings_gear_layout = QVBoxLayout()
        ch_settings_gear_layout.setAlignment(Qt.AlignTop)
        ch_settings_gear_layout.setContentsMargins(0, 0, 11, 0)
        self.setLayout(ch_settings_gear_layout)

        ch_gear_header_label = QLabel("Gear")
        ch_gear_header_label.setStyleSheet("""font-size: 15pt;""")
        ch_gear_header_label.setAlignment(Qt.AlignCenter)

        gear_items_layout = QHBoxLayout()

        gear_items_layout_1 = QVBoxLayout()
        gear_items_layout_2 = QVBoxLayout()
        gear_items_layout_3 = QVBoxLayout()

        gear_items_layout.addLayout(gear_items_layout_1)
        gear_items_layout.addWidget(QVLine())
        gear_items_layout.addLayout(gear_items_layout_2)
        gear_items_layout.addWidget(QVLine())
        gear_items_layout.addLayout(gear_items_layout_3)

        ch_settings_gear_layout.addWidget(ch_gear_header_label)
        ch_settings_gear_layout.addWidget(QHLine())
        ch_settings_gear_layout.addLayout(gear_items_layout)

        item_slots = len(settings_model.equipped_gear)
        for i, gear_slot_entry in enumerate(settings_model.equipped_gear.items()):
            gear_slot = QHBoxLayout()
            gear_slot.setAlignment(Qt.AlignTop)
            gear_slot.setContentsMargins(0, 0, 0, 0)

            gear_lvbox_layout = QVBoxLayout()

            gear_slot_label = QLabel(enums.inventory_slot[gear_slot_entry[0]])
            gear_slot_label.setStyleSheet("""font-size: 11pt;""")
            gear_slot_label.setContentsMargins(4, 0, 0, 0)

            gear_slot_label.setMinimumWidth(65)
            gear_slot_label.setMaximumWidth(65)
            gear_slot_label.setAlignment(Qt.AlignTop)

            self.gear_slot_buttons[i] = QPushButton("Edit")
            self.gear_slot_buttons[i].setMaximumWidth(45)

            gear_lvbox_layout.addWidget(gear_slot_label)
            gear_lvbox_layout.addWidget(self.gear_slot_buttons[i])

            self.gear_slots[i] = GearItem(self.settings_model, gear_slot_entry[0])

            gear_slot.addLayout(gear_lvbox_layout)
            gear_slot.addWidget(self.gear_slots[i])

            current_layout_side = gear_items_layout_1
            if i >= (item_slots / 3) * 2:
                current_layout_side = gear_items_layout_3
            elif i >= (item_slots / 3):
                current_layout_side = gear_items_layout_2

            current_layout_side.addLayout(gear_slot)
            current_layout_side.addWidget(QHLine())

            self.gear_slot_edit_dialog[i] = SelectGearItemDialog(self.settings_model, gear_slot_entry[0])

        self.connect_signals()

    def connect_signals(self):
        for index, edit_button in enumerate(self.gear_slot_buttons.values()):
            inventory_slot = self.gear_slot_edit_dialog[index].inventory_slot
            self.gear_slot_edit_dialog[index].set_dict_signal(self.settings_model.edit_gear_signals[inventory_slot])
            edit_button.clicked.connect(partial(self.open_gear_dialog,
                                                self.gear_slot_edit_dialog[index],
                                                inventory_slot))
        self.settings_model.equipped_gear_signal.connect(self.update_gear_items)

    @pyqtSlot(dict)
    def update_gear_items(self, equipped_items):
        for i, item in enumerate(equipped_items.values()):
            if item.item_id is None:
                self.gear_slots[i].set_empty()
            else:
                if self.gear_slots[i].name_label.text() != item.name:
                    self.gear_slots[i].set_empty()
                self.gear_slots[i].set_name(item.name)

                self.gear_slots[i].set_enchantment(item.can_enchant, item.enchantment)

                self.gear_slots[i].set_sockets([socket["socket_color_name"] for socket in item.sockets.values()])

                self.gear_slots[i].set_sockets_content([socket["socket_content_name"]
                                                        for socket in item.sockets.values()])

    def open_gear_dialog(self, dialog, inv_slot):
        if dialog.list.count() == 0:
            self.settings_model.emit_edit_gear_dict_slot(inv_slot)
        dialog.exec_()


class GearItem(QWidget):

    def __init__(self, model, inventory_slot):
        super().__init__()
        self.model = model
        self.inventory_slot = inventory_slot
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSizeConstraint(QLayout.SetMinimumSize)

        self.name_label = QLabel("--- Slot Empty ---")
        self.name_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.name_label.setStyleSheet("""font-size: 12pt;""")
        self.layout().addWidget(self.name_label)

        self.enchantments = None
        self.enchantment_set_button = None

        self.sockets = None
        self.socket_label = {}
        self.socket_content = {}
        self.socket_buttons = {}

        self.select_enchantment_dialog = SelectEnchantmentDialog(self.model, self.inventory_slot)

        self.select_socket_content_dialog = SelectGemDialog(self.model, self.inventory_slot)

    def set_empty(self):
        if self.enchantments:
            self.layout().removeWidget(self.enchantments)
            self.enchantments = None
        if self.sockets:
            self.layout().removeWidget(self.sockets)
            self.sockets = None
        self.set_name("--- Slot Empty ---")

    def set_name(self, item_name):
        self.name_label.setText(item_name)

    def set_enchantment(self, can_enchant, enchantment):
        if self.enchantments:
            self.layout().removeWidget(self.enchantments)

        if can_enchant:
            self.enchantments = QWidget()
            enchantments_layout = QVBoxLayout()
            enchantments_layout.setContentsMargins(0, 0, 0, 0)
            enchantments_layout.setSizeConstraint(QLayout.SetMinimumSize)
            self.enchantments.setLayout(enchantments_layout)
            if not enchantment:
                enchantment_name = "--- No Enchantment ---"
            else:
                enchantment_name = enchantment[1]

            enchantment_layout = QHBoxLayout()

            enchantment_label = QLabel("Enchantment:")

            enchantment_name_label = QLabel(enchantment_name)
            enchantment_name_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.enchantment_set_button = QPushButton("Edit")
            self.enchantment_set_button.setMaximumWidth(40)

            self.enchantment_set_button.clicked.connect(self.open_enchantments_dialog)

            enchantment_layout.addWidget(enchantment_label)
            enchantment_layout.addWidget(enchantment_name_label)
            enchantment_layout.addWidget(self.enchantment_set_button)
            enchantments_layout.addLayout(enchantment_layout)

            self.layout().addWidget(self.enchantments)

    def set_sockets(self, sockets_colors):
        """
        Display the sockets für this item
        @param:
            sockets     - Required : Tuple with socket colors as bitmask (Tuple)
        """
        if not sockets_colors:
            return

        if self.sockets:
            self.layout().removeWidget(self.sockets)
        self.sockets = QWidget()
        sockets_hlayout = QHBoxLayout()
        sockets_hlayout.setContentsMargins(0, 0, 0, 0)

        sockets_vlayout = QVBoxLayout()
        sockets_vlayout.setContentsMargins(0, 0, 0, 0)

        for index, color_name in enumerate(sockets_colors):
            socket_layout = QHBoxLayout()
            socket_layout.setContentsMargins(0, 0, 0, 0)

            self.socket_label[index] = QLabel(color_name + ":")

            self.socket_content[index] = QLabel("--- No Gem ---")
            self.socket_content[index].setAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.socket_buttons[index] = QPushButton("Edit")
            self.socket_buttons[index].setMaximumWidth(40)

            self.socket_buttons[index].clicked.connect(partial(self.open_socket_dialog, index))

            socket_layout.addWidget(self.socket_label[index])
            socket_layout.addWidget(self.socket_content[index])
            socket_layout.addWidget(self.socket_buttons[index])

            sockets_vlayout.addLayout(socket_layout)

        sockets_label = QLabel("Sockets:")
        sockets_label.setContentsMargins(0, 4, 0, 0)
        sockets_label.setAlignment(Qt.AlignTop)
        sockets_label.setFixedWidth(50)

        sockets_hlayout.addWidget(sockets_label)
        sockets_hlayout.addLayout(sockets_vlayout)

        self.sockets.setLayout(sockets_hlayout)

        self.layout().addWidget(self.sockets)

    def set_sockets_content(self, sockets_content):
        for index, content in enumerate(sockets_content):
            if content:
                self.socket_content[index].setText(content)
            else:
                self.socket_content[index].setText("--- No Gem ---")

    def open_enchantments_dialog(self):
        self.model.set_ench_dict(self.inventory_slot)
        self.select_enchantment_dialog.exec_()

    def open_socket_dialog(self, socket_slot):
        self.select_socket_content_dialog.set_target(socket_slot)
        self.select_socket_content_dialog.exec_()


class SelectGearItemDialog(SelectFromListDialog):
    def __init__(self, model, inventory_slot):
        super().__init__(has_empty_option=True)
        self.model = model
        self.inventory_slot = inventory_slot
        self.on_accept_func = self.select_item
        self.setWindowTitle("Select " + enums.inventory_slot[inventory_slot])

        self.list.setSelectionMode(QAbstractItemView.SingleSelection)

    def select_item(self, item_id):
        self.model.set_gear_slot(self.inventory_slot, item_id)


class SelectEnchantmentDialog(SelectFromListDialog):
    def __init__(self, model, inventory_slot):
        super().__init__(has_empty_option=True)
        self.model = model
        self.inventory_slot = inventory_slot
        self.on_accept_func = self.select_item
        self.resize(QSize(900, 500))

        self.setWindowTitle("Select Enchantment")
        self.set_dict_signal(self.model.enchantment_dict_signal)

        self.list.setSelectionMode(QAbstractItemView.SingleSelection)

    def select_item(self, item_id):
        self.model.set_gear_enchantment(self.inventory_slot, item_id)


class SelectGemDialog(SelectFromListDialog):
    def __init__(self, model, inventory_slot):
        super().__init__(has_empty_option=True)
        self.model = model
        self.inventory_slot = inventory_slot
        self.socket_slot = None
        self.on_accept_func = self.select_item
        self.resize(QSize(900, 500))

        self.setWindowTitle("Select Gem")
        self.set_dict_signal(model.gem_dict_signal)

        self.list.setSelectionMode(QAbstractItemView.SingleSelection)

    def select_item(self, item_id):
        self.model.set_socket_gem(self.inventory_slot, self.socket_slot, item_id)

    def set_target(self, socket_slot):
        self.socket_slot = socket_slot
