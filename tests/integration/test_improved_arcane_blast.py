import unittest
from unittest.mock import Mock

from src.sim.sim_objects.character import Character as Char
from src.sim.sim_objects.enemy import Enemy


class TestImprovedArcaneBlast(unittest.TestCase):
    arcane_blast_rank1 = 30451
    arcane_blast_rank1_mana_cost = 195

    arcane_missiles_rank11_projectile = 38703
    arcane_missiles_rank11 = 38704
    arcane_missiles_rank11_mana_cost = 785

    improved_arcane_blast = 37441

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_increased_damage(self):
        self.char.combat_handler.apply_spell_effect(self.improved_arcane_blast)

        self.assertEqual(1.2, self.char.spell_dmg_multiplier(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.arcane_missiles_rank11_projectile, proc_auras=False))

    def test_increase_resource_cost(self):
        self.char.combat_handler.apply_spell_effect(self.improved_arcane_blast)

        self.assertEqual(round(self.arcane_blast_rank1_mana_cost * 1.2),
                         self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(self.arcane_missiles_rank11_mana_cost,
                         self.char.spell_resource_cost(self.arcane_missiles_rank11, proc_auras=False))
