import sys

import ctypes
from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.gui.models.main_window_model import MainWindowModel
from src.gui.models.sim_settings_model import SimSettingsModel
from src.gui.views.main_window_view import MainWindowView

app_id = u"tbc-dmg-simulation"


def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    app = QApplication(sys.argv)
    with open("../data/style/DarkMode.qss", 'r') as file:
        qss = file.read()
        app.setStyleSheet(qss)

    QFontDatabase.addApplicationFont("../data/fonts/RobotoMono-Medium.ttf")

    settings_model = SimSettingsModel()
    m_window_model = MainWindowModel(settings_model)
    m_window_view = MainWindowView(m_window_model)
    m_window_view.show()

    app.setWindowIcon(QIcon("../data/icons/arcane_intellect.jpg"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
