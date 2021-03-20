import logging.config

import src.db_connector as DB

from src import simulation_settings_loader as SettingsLoader
from src import simulation as Sim
import cProfile

logging.config.fileConfig("logging.conf")


def main():
    if DB.good_startup():
        SettingsLoader.load_settings()
        for i in range(1):
            settings, char = SettingsLoader.get_settings()
            Sim.start_simulation(settings, char)


if __name__ == '__main__':
    # cProfile.run("main()")
    main()
