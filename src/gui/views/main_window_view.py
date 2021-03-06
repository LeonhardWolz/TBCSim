from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
                             QTabWidget, QProgressBar, QTextBrowser, QScrollArea, QMenuBar, QMenu, QAction, QFileDialog,
                             QMessageBox, QDesktopWidget)

from src.gui.views.character_settings_view import CharacterSettingsView
from src.gui.views.results_view import ResultsView
from src.gui.views.sim_settings_view import SimSettingsView


class MainWindowView(QMainWindow):
    ABOUT = "Raid damage simulator for World of Warcraft: The Burning Crusade<br>" \
            "Feel free to contribute at: " \
            "<a href=https://github.com/LeonhardWolz/TBCSim style=\"color: #467fb3;\">" \
            "https://github.com/LeonhardWolz/TBCSim</a><br><br>" \
            "Made using:" \
            "<br>Linea Icons <a href=https://linea.io style=\"color: #467fb3;\">linea.io</a> by Dario Ferrando under " \
            "<a href=https://creativecommons.org/licenses/by/4.0 style=\"color: #467fb3;\">CC BY 4.0</a><br>" \
            "<br>made by Leonhard Wolz, 2021"

    HELP = "This is a raid damage simulator for World of Warcraft: The Burning Crusade<br>" \
           "You can set up your character in the settings tab. You can run the simulation in the simulation tab.<br>" \
           "If you encounter any issues while using this simulator you can create an issue on the Github page " \
           "<a href=https://github.com/LeonhardWolz/TBCSim style=\"color: #467fb3;\">here</a>."

    def __init__(self, mw_model):
        super(QMainWindow, self).__init__()
        self.model = mw_model
        self.character_tabs = []

        self.setWindowTitle('WoW TBC Combat Simulation')
        self.setWindowIcon(QIcon("../data/icons/arcane_intellect.jpg"))
        self.resize(1800, 920)
        self._center()

        self._create_menu_bar()
        self._ui_components()

        self._connect_signals()

        self.model.set_default_values()

    def _center(self):
        geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())

    def _create_menu_bar(self):
        menu_bar = QMenuBar()

        file_menu = QMenu("&Actions", self)

        self.new_action = QAction("&New Sim Settings", self)
        self.new_action.setIcon(QIcon("../data/icons/basic_sheet_txt.svg"))

        self.load_action = QAction("&Load Sim Settings", self)
        self.load_action.setIcon(QIcon("../data/icons/basic_folder_multiple.svg"))
        self.load_action.setShortcut("Ctrl+O")

        self.save_action = QAction("&Save Sim Settings", self)
        self.save_action.setIcon(QIcon("../data/icons/save.svg"))
        self.save_action.setShortcut("Ctrl+S")

        self.exit_action = QAction("&Exit", self)
        self.exit_action.setIcon(QIcon("../data/icons/close.svg"))

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.load_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = QMenu("&Help", self)

        self.help_action = QAction("&Help", self)
        self.help_action.setIcon(QIcon("../data/icons/basic_question.svg"))

        self.about_action = QAction("&About", self)
        self.about_action.setIcon(QIcon("../data/icons/basic_info.svg"))

        help_menu.addAction(self.help_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(help_menu)

        self.setMenuBar(menu_bar)

    def _ui_components(self):
        central_widget = QWidget()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 4, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._simulation_settings_tab(), "Simulation Settings")
        #self.tabs.addTab(self._character_settings_tab(self.model.settings_model.character_settings[0]), "Character Settings")
        self.tabs.addTab(ResultsView(self.model), "Simulation")

        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def _simulation_settings_tab(self):
        settings_scroll_area = QScrollArea()
        settings_scroll_area.setWidgetResizable(True)
        settings_scroll_area.setWidget(SimSettingsView(self.model.settings_model))

        return settings_scroll_area

    def _character_settings_tab(self, model):
        character_settings_scroll_area = QScrollArea()
        character_settings_scroll_area.setWidgetResizable(True)
        character_settings_scroll_area.setWidget(CharacterSettingsView(model))

        return character_settings_scroll_area

    def _connect_signals(self):
        self.new_action.triggered.connect(self.model.new_sim_settings)
        self.load_action.triggered.connect(self._load_sim_settings)
        self.save_action.triggered.connect(self._save_sim_settings)

        self.about_action.triggered.connect(self.open_about)
        self.help_action.triggered.connect(self.open_help)

        self.exit_action.triggered.connect(self.close)

        self.model.settings_model.character_settings_signal.connect(self._load_character_tabs)

    @pyqtSlot(list)
    def _load_character_tabs(self, value):
        for character_tab in self.character_tabs:
            self.tabs.removeTab(self.tabs.indexOf(character_tab))
        self.character_tabs = []
        for x, char_settings in enumerate(value):
            tab = self._character_settings_tab(char_settings)
            self.character_tabs.append(tab)
            self.tabs.insertTab(1, tab, "Character Settings " + str(x+1))

    def _load_sim_settings(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Load Sim Settings")
        dialog.setNameFilter("(*.yml)")
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec_()
        if dialog.selectedFiles():
            self.model.load_sim_settings(dialog.selectedFiles())

    def _save_sim_settings(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save Sim Settings")
        dialog.setNameFilter("(*.yml)")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec_()
        if dialog.selectedFiles():
            self.model.save_sim_settings(dialog.selectedFiles())

    def open_help(self):
        about_window = QMessageBox()
        about_window.setTextFormat(Qt.RichText)
        about_window.setWindowTitle("Help")
        about_window.setText(self.HELP)
        about_window.setIconPixmap(QPixmap("../data/icons/basic_info.svg"))
        about_window.setStandardButtons(QMessageBox.Ok)
        about_window.exec_()

    def open_about(self):
        about_window = QMessageBox()
        about_window.setTextFormat(Qt.RichText)
        about_window.setWindowTitle("About")
        about_window.setText(self.ABOUT)
        about_window.setIconPixmap(QPixmap("../data/icons/basic_info.svg"))
        about_window.setStandardButtons(QMessageBox.Ok)
        about_window.exec_()

    def closeEvent(self, close_event) -> None:
        close_msg = "Unsaved settings will be lost. Are you sure you want to quit?"
        close_window = QMessageBox()
        close_window.setWindowTitle("Quit?")
        close_window.setText(close_msg)
        close_window.setIconPixmap(QPixmap("../data/icons/basic_question.svg"))
        close_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        close_window.setDefaultButton(QMessageBox.No)
        reply = close_window.exec_()

        if reply == QMessageBox.Yes:
            close_event.accept()
        else:
            close_event.ignore()
