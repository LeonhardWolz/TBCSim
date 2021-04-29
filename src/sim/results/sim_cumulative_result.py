import os
from dataclasses import dataclass

row_divider = "---------------------------------------------------------------" \
              "---------------------------------------------------------------"


@dataclass
class SimCumResult:
    def __init__(self):
        self.settings = None
        self.results = None
        self.start_time = None
        self.run_time = None
        self.errors = []

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def run_time(self):
        return self._run_time

    @run_time.setter
    def run_time(self, value):
        self._run_time = value

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value

    def all_errors_short(self):
        return self.errors + [result.errors_short for result in self.results if result.errors_short != ""]

    def __str__(self):
        str_repr = "Results for TBC Combat Simulation from: {}\n\n".format(
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"))

        str_repr += "Simulation Settings\n"
        str_repr += "-----------------------------------------\n"
        str_repr += f"Simulation Type: {self.settings.sim_type}\n"
        str_repr += f"Length of Simulation: {str(self.settings.sim_duration / 1000)}s\n"
        str_repr += f"Iterations: {self.settings.sim_iterations}\n"

        str_repr += "\n"
        str_repr += "Best Single Simulation by DPS Results:\n"
        str_repr += row_divider
        str_repr += str(max(self.results, key=lambda res: res.dps))
        str_repr += row_divider

        str_repr += "\n\n----------------------------- Cumulative Sim Results -----------------------------"
        str_repr += f"\nCompleted {self.settings.sim_iterations} Iteration(s) in {self.run_time} seconds"
        str_repr += f"\n\nAvg DPS: {self.avg_dps}"

        if self.errors:
            str_repr += "\n\nErrors during Simulation:\n"
            str_repr += "-----------------------------------------\n"
            for x, error in enumerate(self.all_errors_short()):
                str_repr += f"Error {x+1}:    " + error + "\n\n"
            str_repr += "\n\n"

        return str_repr

    @property
    def avg_dps(self):
        return round(sum([res.dps for res in self.results]) / self.settings.sim_iterations, 2)

    def write_result_files(self):
        file_path = self.settings.results_file_path
        if file_path is None:
            file_path = os.getcwd()

        if self.settings.full_log_for_best:
            with open(file_path + "Full_Combat_Log_Best_Sim_"
                      + self.start_time.strftime("%Y_%m_%d-%H_%M_%S") + ".log", "w") as file:
                file.write(max(self.results, key=lambda res: res.dps).full_combat_log)

        with open(file_path + "Complete_Sim_Result_"
                  + self.start_time.strftime("%Y_%m_%d-%H_%M_%S") + ".txt", "w") as file:
            file.write(str(self))
