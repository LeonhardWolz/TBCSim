from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QHBoxLayout, QPushButton, QProgressBar, QFileDialog


class ResultsView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        results_vbox_layout = QVBoxLayout()
        results_vbox_layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(results_vbox_layout)

        self.results_text_browser = QTextBrowser()
        self.results_text_browser.setLineWrapMode(QTextBrowser.NoWrap)

        results_vbox_layout.addLayout(self._controls_layout())
        results_vbox_layout.addWidget(self.results_text_browser)

        self._connect_signals()

    def _controls_layout(self):
        controls_hlayout = QHBoxLayout()

        self.start_sim_button = QPushButton("Run Simulation", parent=self)
        self.start_sim_button.setFixedSize(150, 24)

        self.sim_progress_bar = QProgressBar()
        self.sim_progress_bar.setTextVisible(True)
        self.sim_progress_bar.setAlignment(Qt.AlignCenter)
        self.sim_progress_bar.setFixedHeight(22)

        self.save_results_button = QPushButton("Save Results", parent=self)
        self.save_results_button.setFixedSize(110, 24)

        controls_hlayout.addWidget(self.start_sim_button, 0)
        controls_hlayout.addWidget(self.sim_progress_bar, 1)
        controls_hlayout.addWidget(self.save_results_button, 2)

        return controls_hlayout

    def _connect_signals(self):
        self.start_sim_button.clicked.connect(self.model.start_sim)
        self.save_results_button.clicked.connect(self._save_sim_results)

        self.model.progress.connect(self.progress_value)
        self.model.progress_label.connect(self.progress_label)
        self.model.sim_button_enabled.connect(self.sim_button_enabled)
        self.model.results_text.connect(self.results_text_output)

    def _save_sim_results(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save Sim Results")
        dialog.setNameFilter("(*.txt)")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec_()
        if dialog.selectedFiles():
            self.model.save_sim_results(dialog.selectedFiles())

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