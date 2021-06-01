from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QLabel, QLineEdit, QWidget, QListWidgetItem)


class SelectFromListDialog(QDialog):
    def __init__(self, on_accept_func=None, has_empty_option=False):
        super().__init__()
        self.on_accept_func = on_accept_func
        self.empty_option = has_empty_option

        self.resize(QSize(600, 500))

        buttons = QDialogButtonBox()
        buttons.addButton("Add", QDialogButtonBox.AcceptRole)
        buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(QVBoxLayout())
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.layout().addWidget(self.list)

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.addWidget(QLabel("Search:"))
        self.input = QLineEdit()
        search_layout.addWidget(self.input)
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        self.layout().addWidget(search_widget)
        self.layout().addWidget(buttons)

        self.input.textChanged.connect(self.on_text_changed)
        self.list.doubleClicked.connect(self.accept)

        self.input.setFocus()

    def set_dict_signal(self, signal):
        signal.connect(self.list_content)

    def accept(self):
        for item in self.list.selectedItems():
            self.on_accept_func(item.object_id)
        super(SelectFromListDialog, self).accept()

    def exec_(self):
        self.input.setText("")
        self.input.setFocus()
        super(SelectFromListDialog, self).exec_()

    @pyqtSlot(dict)
    def list_content(self, dictionary):
        self.list.clear()
        if self.empty_option:
            QListWidgetItemID("{:7s}{:50s}".format("0", "-- Empty --"), self.list, 0)
        for index, item in enumerate(dictionary.items()):
            item_label = "{:7s}".format(str(item[0]))
            for string in item[1]:
                item_label += "{:50s}".format(string)
            QListWidgetItemID(item_label, self.list, item[0])

    @pyqtSlot(str)
    def on_text_changed(self, text):
        for row in range(self.list.count()):
            item = self.list.item(row)
            if text:
                item.setHidden(not text.lower() in item.text().lower())
            else:
                item.setHidden(False)


class QListWidgetItemID(QListWidgetItem):
    def __init__(self, name=None, parent=None, object_id=None):
        super(QListWidgetItemID, self).__init__(name, parent)
        self.object_id = object_id
