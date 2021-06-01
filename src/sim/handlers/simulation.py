from datetime import datetime
import traceback

import simpy
from profilehooks import profile

from src.sim.logic.player import Player
from src.sim.results.sim_results import SimResult

#@profile(immediate=True, entries=100, sort="tottime")
def start_simulation(settings, char, sim_num):
    env = simpy.Environment()
    results = SimResult(start_time=datetime.now(), sim_length=settings.sim_duration)
    results.set_items(char.gear)
    results.info("Starting Simulation for " + str(settings.sim_duration / 1000) + " seconds.")
    char.combat_handler.env = env
    char.combat_handler.results = results
    char.combat_handler.sim_num = sim_num
    # noinspection PyBroadException
    try:
        player = Player(env, char, results, settings.sim_combat_rater)
        env.process(player.rotation())
        env.process(player.mana_regeneration())
        env.run(until=settings.sim_duration)
    except Exception as ex:
        results.errors_short = f"Error during Simulation Nr. {sim_num + 1}\n" \
                               f"{traceback.format_exc()}"

    return results
