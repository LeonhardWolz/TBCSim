from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
                             QTabWidget, QProgressBar, QTextBrowser, QScrollArea, QMenuBar, QMenu, QAction, QFileDialog)

from src.gui.views.settings_view import SettingsView


class MainWindowView(QMainWindow):
    def __init__(self, mw_model):
        super(QMainWindow, self).__init__()
        self.model = mw_model

        self.setWindowTitle('WoW TBC Combat Simulation')
        self.setWindowIcon(QIcon("arcane_intellect.jpg"))
        self.resize(1600, 900)
        self._create_menu_bar()
        self._ui_components()

        self._connect_signals()

        self.model.set_default_values()

    def _create_menu_bar(self):
        menu_bar = QMenuBar()

        file_menu = QMenu("&Actions", self)

        self.new_action = QAction("&New Sim Settings", self)
        self.load_action = QAction("&Load Sim Settings", self)
        self.save_action = QAction("&Save Sim Settings", self)
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action = QAction("&Exit", self)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.load_action)
        file_menu.addAction(self.save_action)
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

        results_vbox_layout.addWidget(self.results_text_browser)
        results_vbox_layout.addLayout(self._controls_layout())

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
