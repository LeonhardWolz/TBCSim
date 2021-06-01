import concurrent.futures
import time
from datetime import datetime

import src.db.db_connector as DB

from src.sim.settings import simulation_settings_loader as SettingsLoader
from src.sim.handlers import simulation as Sim
from src.sim.results.sim_cumulative_result import SimCumResult


class SimHandler(object):
    def __init__(self):
        self.sim_cum_results = None
        self.completed_sims = 0

        if not DB.good_startup():
            raise ConnectionError

    def run_simulations(self):
        sim_start_time = time.perf_counter()
        sim_results = []
        SettingsLoader.load_settings()
        sim_settings = SettingsLoader.get_sim_settings()
        self.print_progress_bar(self.completed_sims, sim_settings.sim_iterations)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for sim_num in range(sim_settings.sim_iterations):
                settings, char = SettingsLoader.get_settings()
                sim_results.append(executor.submit(Sim.start_simulation, settings, char, sim_num))

            for _ in concurrent.futures.as_completed(sim_results):
                self.completed_sims += 1
                self.print_progress_bar(self.completed_sims, settings.sim_iterations)

        sim_end_time = time.perf_counter()
        self.sim_cum_results = SimCumResult(sim_settings,
                                            [res.result() for res in sim_results],
                                            datetime.now(),
                                            round(sim_end_time - sim_start_time, 2))

        self.sim_cum_results.write_result_files()
        print(self.sim_cum_results)

    # Print iterations progress
    def print_progress_bar(self, iteration, total, prefix='Progress', suffix='of Simulations Complete',
                           decimals=1, length=100, fill='█', print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {iteration}/{total} {suffix}', end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()
