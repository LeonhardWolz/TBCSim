import unittest
from unittest.mock import MagicMock

from src.sim.sim_objects import character, aura


class AuraSpellPowerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.char = character.Character()
        self.value = 18
        spell_power_aura = aura.Aura(9346, 13, self.value, 126, 0, 8)
        self.char.combat_handler.active_auras.append(spell_power_aura)

    def test_fire_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(4))

    def test_total_fire_power(self):
        self.assertEqual(self.value, self.char.total_fire_power)

    def test_holy_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(2))

    def test_total_holy_power(self):
        self.assertEqual(self.value, self.char.total_holy_power)

    def test_frost_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(16))

    def test_total_frost_power(self):
        self.assertEqual(self.value, self.char.total_frost_power)

    def test_nature_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(8))

    def test_total_nature_power(self):
        self.assertEqual(self.value, self.char.total_nature_power)

    def test_shadow_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(32))

    def test_total_shadow_power(self):
        self.assertEqual(self.value, self.char.total_shadow_power)

    def test_arcane_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(64))

    def test_total_arcane_power(self):
        self.assertEqual(self.value, self.char.total_arcane_power)


class AuraFirePowerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.char = character.Character()
        self.value = 13
        fire_power_aura = aura.Aura(9400, 13, self.value, 4, 0, 8)
        self.char.combat_handler.active_auras.append(fire_power_aura)

    def test_fire_power_from_auras(self):
        self.assertEqual(self.value, self.char.school_power_from_auras(4))

    def test_total_fire_power(self):
        self.assertEqual(self.value, self.char.total_fire_power)

    def test_holy_power_from_auras(self):
        self.assertEqual(0, self.char.school_power_from_auras(2))

    def test_total_holy_power(self):
        self.assertEqual(0, self.char.total_holy_power)

    def test_frost_power_from_auras(self):
        self.assertEqual(0, self.char.school_power_from_auras(16))

    def test_total_frost_power(self):
        self.assertEqual(0, self.char.total_frost_power)

    def test_nature_power_from_auras(self):
        self.assertEqual(0, self.char.school_power_from_auras(8))

    def test_total_nature_power(self):
        self.assertEqual(0, self.char.total_nature_power)

    def test_shadow_power_from_auras(self):
        self.assertEqual(0, self.char.school_power_from_auras(32))

    def test_total_shadow_power(self):
        self.assertEqual(0, self.char.total_shadow_power)

    def test_arcane_power_from_auras(self):
        self.assertEqual(0, self.char.school_power_from_auras(64))

    def test_total_arcane_power(self):
        self.assertEqual(0, self.char.total_arcane_power)


def spell_cast_time(spell_id):
    if spell_id == 38697:
        return 3000
    elif spell_id == 38692:
        return 3500


def spell_family_flags(spell_id):
    if spell_id == 38697:
        return 32
    elif spell_id == 38692:
        return 1


def spell_school(spell_id):
    if spell_id == 38697:
        return 16
    elif spell_id == 38692:
        return 4


def spell_power_coeff(spell_id):
    if spell_id == 38697:
        return spell_cast_time(spell_id) / 3500
    elif spell_id == 38692:
        return spell_cast_time(spell_id) / 3500


class AuraSpellModTest(unittest.TestCase):
    def setUp(self) -> None:
        self.char = character.Character()
        self.char.combat_handler.spell_cast_time = MagicMock(side_effect=spell_cast_time)
        self.char.combat_handler.spell_family_mask = MagicMock(side_effect=spell_family_flags)
        self.char.combat_handler.spell_school = MagicMock(side_effect=spell_school)
        self.char.combat_handler.spell_power_coefficient = MagicMock(side_effect=spell_power_coeff)
        self.char.combat_handler.enemy = MagicMock()
        self.char.combat_handler.enemy.active_auras = {}
        self.char.player_class = "Mage"

        self.cast_time_mod = -200
        improved_frostbolt = aura.Aura(spell_id=12473,
                                       aura_id=107,
                                       value=self.cast_time_mod,
                                       misc_value=10,
                                       affected_spell_family_mask=32,
                                       affected_spell_school=16)
        self.char.combat_handler.active_auras.append(improved_frostbolt)

        self.spell_power_coeff_mod = 2
        empowered_frostbolt1 = aura.Aura(spell_id=31682,
                                         aura_id=107,
                                         value=self.spell_power_coeff_mod,
                                         misc_value=24,
                                         affected_spell_family_mask=32,
                                         affected_spell_school=16)
        self.char.combat_handler.active_auras.append(empowered_frostbolt1)

        self.spell_crit_chance_mod = 1
        empowered_frostbolt2 = aura.Aura(spell_id=31682,
                                         aura_id=107,
                                         value=self.spell_crit_chance_mod,
                                         misc_value=7,
                                         affected_spell_family_mask=32,
                                         affected_spell_school=16)
        self.char.combat_handler.active_auras.append(empowered_frostbolt2)

    def test_frostbolt_cast_time_mod(self):
        self.assertEqual(3000 + self.cast_time_mod, self.char.spell_cast_time(38697))

    def test_fireball_cast_time_mod(self):
        self.assertEqual(3500, self.char.spell_cast_time(38692))

    def test_frostbolt_coefficient(self):
        self.assertEqual(round(3000 / 3500 + self.spell_power_coeff_mod / 100, 3),
                         self.char.spell_power_coefficient(38697))

    def test_fireball_coefficient(self):
        self.assertEqual(3500 / 3500, self.char.spell_power_coefficient(38692))

    def test_frostbolt_crit_chance(self):
        self.assertEqual(1.91, self.char.spell_crit_chance_spell(38697))

    def test_fireball_crit_chance(self):
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(38692))


if __name__ == '__main__':
    unittest.main()
