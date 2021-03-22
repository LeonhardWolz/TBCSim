from dataclasses import dataclass


@dataclass
class SimSettings:
    sim_type: str = ""
    sim_duration: int = 0
    sim_iterations: int = 0
    results_file_path: str = None
    full_log_for_best: bool = False

