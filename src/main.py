import concurrent.futures
import time
from datetime import datetime

import src.db_connector as DB

from src import simulation_settings_loader as SettingsLoader
from src import simulation as Sim
from src.sim_cumulative_result import SimCumResult


def main():
    if DB.good_startup():
        sim_start_time = time.perf_counter()
        sim_results = []
        SettingsLoader.load_settings()
        sim_settings = SettingsLoader.get_sim_settings()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for sim_num in range(sim_settings.sim_iterations):
                settings, char = SettingsLoader.get_settings()
                sim_results.append(executor.submit(Sim.start_simulation, settings, char, sim_num))

        sim_end_time = time.perf_counter()
        sim_cum_results = SimCumResult(sim_settings,
                                       [res.result() for res in sim_results],
                                       datetime.now(),
                                       round(sim_end_time - sim_start_time, 2))

        sim_cum_results.write_result_files()
        print(sim_cum_results)


if __name__ == '__main__':
    # cProfile.run("main()", sort="cumtime")
    main()
