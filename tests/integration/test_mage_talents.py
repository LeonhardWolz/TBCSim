import unittest

from src.aura import Aura
from src.character import Character as Char


class TestArcaneSubtlety(unittest.TestCase):
    rank1 = 11210
    rank2 = 12592

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arcane_subltety_rank1(self):
        self.assertEqual(True, False)

    def test_arcane_subltety_rank2(self):
        self.assertEqual(True, False)


class TestArcaneFocus(unittest.TestCase):
    rank1 = 11222
    rank2 = 12839
    rank3 = 12840
    rank4 = 12841
    rank5 = 12842

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arcane_focus_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.rank1)

        self.assertEqual(self.char.spell_hit_chance + 2, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.rank2)

        self.assertEqual(self.char.spell_hit_chance + 4, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.rank3)

        self.assertEqual(self.char.spell_hit_chance + 6, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.rank4)

        self.assertEqual(self.char.spell_hit_chance + 8, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.rank5)

        self.assertEqual(self.char.spell_hit_chance + 10, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))


class TestImprovedArcaneMissiles(unittest.TestCase):
    improved_arcane_missiles_rank1 = 31579
    improved_arcane_missiles_rank2 = 31582
    improved_arcane_missiles_rank3 = 31583
    arcane_missiles_rank1 = 5143
    mana_cost_arcane_missiles_rank1 = 85

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_arcane_missiles_rank1(self):
        self.assertEqual(True, False)


class TestWandSpecialization(unittest.TestCase):
    wand_specialization_rank1 = 6057
    wand_specialization_rank2 = 6085

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_wand_specialization_rank1(self):
        self.assertEqual(True, False)


class TestArcaneConcentration(unittest.TestCase):
    arcane_concentration_rank1 = 11213

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.apply_spell_effect(self.arcane_concentration_rank1)
        for aura in self.char.spell_handler.active_auras:
            aura.proc[1] = 100

    def test_arcane_concentration(self):
        self.assertEqual(30, self.char.spell_resource_cost(133, True))
        self.char.process_on_spell_hit(133)
        self.assertEqual(0, self.char.spell_resource_cost(133, True))
        self.assertEqual(30, self.char.spell_resource_cost(133, True))


class TestMagicAttunement(unittest.TestCase):
    magic_attunement_rank1 = 11247
    magic_attunement_rank2 = 12606

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_magic_attunement_rank1(self):
        self.assertEqual(True, False)


class TestArcaneImpact(unittest.TestCase):
    arcane_impact_rank1 = 11242
    arcane_impact_rank2 = 12467
    arcane_impact_rank3 = 12469

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arcane_impact_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.arcane_impact_rank1)
        self.assertEqual(2, self.char.spell_crit_chance_spell(30451))
        self.assertEqual(0, self.char.spell_crit_chance_spell(133))

    def test_arcane_impact_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.arcane_impact_rank2)
        self.assertEqual(4, self.char.spell_crit_chance_spell(30451))
        self.assertEqual(0, self.char.spell_crit_chance_spell(133))

    def test_arcane_impact_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.arcane_impact_rank3)
        self.assertEqual(6, self.char.spell_crit_chance_spell(30451))
        self.assertEqual(0, self.char.spell_crit_chance_spell(133))


class ArcaneFortitude(unittest.TestCase):
    arcane_fortitude_rank1 = 28574

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arcane_fortitude(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
