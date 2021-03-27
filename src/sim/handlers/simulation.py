from datetime import datetime

import simpy

from src.sim.logic.player import Player
from src.results.sim_results import SimResult


def start_simulation(settings, char, sim_num):
    env = simpy.Environment()
    results = SimResult(start_time=datetime.now(), sim_length=settings.sim_duration)
    results.set_items(char.gear)
    results.info("Starting Simulation for " + str(settings.sim_duration / 1000) + " seconds.")
    char.spell_handler.env = env
    char.spell_handler.results = results
    char.spell_handler.sim_num = sim_num
    player = Player(env, char, results, settings.sim_combat_rater)
    env.process(player.rotation())
    env.process(player.mana_regeneration())
    env.run(until=settings.sim_duration)
    return results
