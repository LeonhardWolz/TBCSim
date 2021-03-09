from datetime import datetime

import simpy
import logging

from src.player import Player
from src.sim_results import SimResult

logger = logging.getLogger("simulation")


def start_simulation(settings, char):
    logger.warning("Starting Simulation for " + str(settings.duration / 1000) + " seconds.")
    env = simpy.Environment()
    results = SimResult(start_time=datetime.now(), sim_length=settings.duration)
    results.set_items(char.items)
    char.spell_handler.env = env
    char.spell_handler.results = results
    player = Player(env, char, results)
    env.process(player.rotation())
    env.process(player.mana_regeneration())
    env.run(until=settings.duration)
    print(results)


def print_results(settings, char):
    logger.warning("Simulation Complete")
    logger.warning("Total damage: " + str(char.spell_handler.enemy.total_damage_taken))
    logger.warning("DPS: " + str(char.spell_handler.enemy.total_damage_taken / (settings.duration / 1000)))
