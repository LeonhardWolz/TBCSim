import sys

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
                             QTabWidget, QProgressBar, QTextBrowser, QScrollArea, QMenuBar, QMenu, QAction, QFileDialog,
                             QMessageBox)

from src.gui.views.settings_view import SettingsView


class MainWindowView(QMainWindow):
    ABOUT = "DMG Simulation for World of Warcraft TBC<br>" \
            "Feel free to contribute at: " \
            "<a href=https://github.com/LeonhardWolz/TBCSim>https://github.com/LeonhardWolz/TBCSim</a><br><br>" \
            "Made using:" \
            "<br>Linea Icons <a href=https://linea.io>linea.io</a> by Dario Ferrando under " \
            "<a href=https://creativecommons.org/licenses/by/4.0>CC BY 4.0</a><br>" \
            "<br>made by Leonhard Wolz, 2021"

    def __init__(self, mw_model):
        super(QMainWindow, self).__init__()
        self.model = mw_model

        self.setWindowTitle('WoW TBC Combat Simulation')
        self.setWindowIcon(QIcon("icons/arcane_intellect.jpg"))
        self.resize(1600, 900)
        self._create_menu_bar()
        self._ui_components()

        self._connect_signals()

        self.model.set_default_values()

    def _create_menu_bar(self):
        menu_bar = QMenuBar()

        file_menu = QMenu("&Actions", self)

        self.new_action = QAction("&New Sim Settings", self)
        self.new_action.setIcon(QIcon("icons/basic_sheet_txt .svg"))
        self.load_action = QAction("&Load Sim Settings", self)
        self.load_action.setIcon(QIcon("icons/basic_folder.svg"))
        self.save_action = QAction("&Save Sim Settings", self)
        self.save_action.setIcon(QIcon("icons/basic_floppydisk.svg"))
        self.save_action.setShortcut("Ctrl+S")
        self.about_action = QAction("&About", self)
        self.about_action.setIcon(QIcon("icons/basic_info.svg"))
        self.exit_action = QAction("&Exit", self)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.load_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.about_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        menu_bar.addMenu(file_menu)

        self.setMenuBar(menu_bar)

    def _ui_components(self):
        central_widget = QWidget()

        main_layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(self._settings_tab(), "Settings")
        tabs.addTab(self._results_tab(), "Simulation")

        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def _controls_layout(self):
        controls_hlayout = QHBoxLayout()

        self.start_sim_button = QPushButton("Run Simulation", parent=self)
        self.start_sim_button.setFixedSize(150, 24)
        button_font = self.start_sim_button.font()
        button_font.setPointSize(10)
        self.start_sim_button.setFont(button_font)

        self.sim_progress_bar = QProgressBar()
        self.sim_progress_bar.setTextVisible(True)
        self.sim_progress_bar.setAlignment(Qt.AlignCenter)
        self.sim_progress_bar.setFixedHeight(22)

        controls_hlayout.addWidget(self.start_sim_button, 0)
        controls_hlayout.addWidget(self.sim_progress_bar, 1)

        return controls_hlayout

    def _settings_tab(self):
        settings_scroll_area = QScrollArea()
        settings_scroll_area.setWidgetResizable(True)
        settings_scroll_area.setWidget(SettingsView(self.model.settings_model))

        return settings_scroll_area

    def _results_tab(self):
        results_widget = QWidget()

        results_vbox_layout = QVBoxLayout()
        results_widget.setLayout(results_vbox_layout)

        self.results_text_browser = QTextBrowser()
        self.results_text_browser.setLineWrapMode(QTextBrowser.NoWrap)
        self.results_text_browser.setFont(QFont("Courier"))

        results_vbox_layout.addLayout(self._controls_layout())
        results_vbox_layout.addWidget(self.results_text_browser)

        return results_widget

    def _connect_signals(self):
        self.start_sim_button.clicked.connect(self.model.start_sim)

        self.model.progress.connect(self.progress_value)
        self.model.progress_label.connect(self.progress_label)
        self.model.sim_button_enabled.connect(self.sim_button_enabled)
        self.model.results_text.connect(self.results_text_output)

        self.new_action.triggered.connect(self.model.new_sim_settings)
        self.load_action.triggered.connect(self._load_sim_settings)
        self.save_action.triggered.connect(self._save_sim_settings)

        self.about_action.triggered.connect(self.open_about)

        self.exit_action.triggered.connect(self.close)

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

    def open_about(self):
        about_window = QMessageBox()
        about_window.setTextFormat(Qt.RichText)
        about_window.setWindowTitle("About")
        about_window.setText(self.ABOUT)
        about_window.setIconPixmap(QPixmap("icons/basic_info.svg"))
        about_window.setStandardButtons(QMessageBox.Ok)
        about_window.exec_()

    def closeEvent(self, close_event) -> None:
        close_msg = "Unsaved settings will be lost. Are you sure you want to quit?"
        close_window = QMessageBox()
        close_window.setWindowTitle("Quit?")
        close_window.setText(close_msg)
        close_window.setIconPixmap(QPixmap("icons/basic_question.svg"))
        close_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        close_window.setDefaultButton(QMessageBox.No)
        reply = close_window.exec_()

        if reply == QMessageBox.Yes:
            close_event.accept()
        else:
            close_event.ignore()

    @pyqtSlot(int)
    def progress_value(self, value):
        self.sim_progress_bar.setValue(value)

    @pyqtSlot(str)
    def progress_label(self, value):
        self.sim_progress_bar.setFormat(value)

    @pyqtSlot(bool)
    def sim_button_enabled(self, value):
        self.start_sim_button.setEnabled(value)

    @pyqtSlot(str)
    def results_text_output(self, value):
        self.results_text_browser.setText(value)
        self.results_text_browser.verticalScrollBar().setValue(self.results_text_browser.verticalScrollBar().maximum())
