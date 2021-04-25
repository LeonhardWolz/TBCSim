import time
import concurrent.futures
from datetime import datetime

import yaml
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

import src.db.db_connector as DB
from src.sim.handlers import simulation as Sim
from src.sim.results.sim_cumulative_result import SimCumResult
from src.sim.settings.simulation_settings_loader import SimulationSettingsLoader


class MainWindowModel(QObject):
    progress = pyqtSignal(int)
    progress_label = pyqtSignal(str)
    sim_button_enabled = pyqtSignal(bool)
    results_text = pyqtSignal(str)

    def __init__(self, settings_model):
        super().__init__()
        self.settings_model = settings_model
        self.last_results = None
        self.sim_thread = None
        self.sim_worker = None
        self.results = None

    def set_default_values(self):
        self.progress_label.emit("0/0 0.00%")
        self.progress.emit(0)
        self.sim_button_enabled.emit(True)
        self.results_text.emit("")

    @pyqtSlot(name="start_sim")
    def start_sim(self):
        self.sim_thread = QThread()
        self.sim_worker = SimWorker(self, SimulationSettingsLoader(self.settings_model.settings_dict))

        self.sim_worker.moveToThread(self.sim_thread)
        self.sim_thread.started.connect(self.sim_worker.run_simulations)

        self.sim_worker.finished.connect(self.sim_thread.quit)
        self.sim_worker.finished.connect(self.sim_worker.deleteLater)
        self.sim_thread.finished.connect(self.sim_thread.deleteLater)

        self.sim_thread.finished.connect(self.populate_results)

        self.sim_thread.start()

    def populate_results(self):
        self.results_text.emit(str(self.sim_worker.sim_cum_results))
        self.last_results = self.sim_worker.sim_cum_results

    def new_sim_settings(self):
        self.settings_model.set_default()

    def load_sim_settings(self, load_file_name):
        with open(fr"{load_file_name[0]}", "r") as file:
            settings_dict = yaml.safe_load(file)
        self.settings_model.load_from_dict(settings_dict)

    def save_sim_settings(self, save_file_name):
        with open(fr"{save_file_name[0]}", "w") as file:
            yaml.dump(self.settings_model.settings_dict, file)


class SimWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, model, settings_loader):
        super().__init__()
        self.model = model
        self.settings_loader = settings_loader
        self.sim_cum_results = None
        self.completed_sims = 0

        if not DB.good_startup():
            raise ConnectionError

    @pyqtSlot()
    def run_simulations(self):
        self.model.progress_label.emit("0/0 0.00%")
        self.model.progress.emit(0)
        self.model.sim_button_enabled.emit(False)
        self.model.results_text.emit("Simulating...")

        sim_start_time = time.perf_counter()
        sim_results = []
        sim_settings = self.settings_loader.get_sim_settings()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for sim_num in range(sim_settings.sim_iterations):
                settings, char = self.settings_loader.get_settings()
                sim_results.append(executor.submit(Sim.start_simulation, settings, char, sim_num))

            for _ in concurrent.futures.as_completed(sim_results):
                self.completed_sims += 1
                self.model.progress.emit(int((self.completed_sims / sim_settings.sim_iterations) * 100))
                self.model.progress_label.emit(str(self.completed_sims) + "/" + str(sim_settings.sim_iterations) + " "
                                               + "%0.2f" % ((self.completed_sims / sim_settings.sim_iterations) * 100)
                                               + "%")

        sim_end_time = time.perf_counter()
        self.sim_cum_results = SimCumResult(sim_settings,
                                            [res.result() for res in sim_results],
                                            datetime.now(),
                                            round(sim_end_time - sim_start_time, 2))
        self.model.progress_label.emit(str(self.completed_sims) + "/" + str(sim_settings.sim_iterations) + " "
                                       + "%0.2f" % ((self.completed_sims / sim_settings.sim_iterations) * 100)
                                       + "% - Simulation Complete")

        self.model.sim_button_enabled.emit(True)
        # print("done")
        self.finished.emit()
        # self.sim_cum_results.write_result_files()
        # print(self.sim_cum_results)
