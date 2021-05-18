import unittest
from unittest.mock import Mock

from src.sim.sim_objects.character import Character as Char
from src.sim.sim_objects.enemy import Enemy


class TestArcaneBlast(unittest.TestCase):
    arcane_blast_rank1 = 30451

    arcane_blast_debuff = 36032

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.results = Mock()
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0

    def test_arcane_blast_debuff_application(self):
        self.char.spell_handler.apply_spell_effect(self.arcane_blast_rank1)
        self.assertTrue(self.arcane_blast_debuff in [aura.spell_id for aura in self.char.spell_handler.active_auras])

    def test_arcane_blast_debuff_effect(self):
        self.assertEqual(2500, self.char.spell_cast_time(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(195, self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(self.arcane_blast_debuff)
        self.assertEqual(2500 - 334, self.char.spell_cast_time(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(round(195 * 1.75), self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(self.arcane_blast_debuff)
        self.assertEqual(2500 - 334 * 2, self.char.spell_cast_time(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(round(195 * 2.5), self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(self.arcane_blast_debuff)
        self.assertEqual(2500 - 334 * 3, self.char.spell_cast_time(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(round(195 * 3.25), self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(self.arcane_blast_debuff)
        self.assertEqual(2500 - 334 * 3, self.char.spell_cast_time(self.arcane_blast_rank1, proc_auras=False))
        self.assertEqual(round(195 * 3.25), self.char.spell_resource_cost(self.arcane_blast_rank1, proc_auras=False))
