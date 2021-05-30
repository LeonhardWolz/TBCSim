import unittest

from src.sim.sim_objects.character import Character as Char
from src.sim.sim_objects.enemy import Enemy


@unittest.skip("Not yet implemented")
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
        self.char.combat_handler.apply_spell_effect(self.rank1)

        self.assertEqual(self.char.spell_hit_chance + 2, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.rank2)

        self.assertEqual(self.char.spell_hit_chance + 4, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.rank3)

        self.assertEqual(self.char.spell_hit_chance + 6, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank4(self):
        self.char.combat_handler.apply_spell_effect(self.rank4)

        self.assertEqual(self.char.spell_hit_chance + 8, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))

    def test_arcane_focus_rank5(self):
        self.char.combat_handler.apply_spell_effect(self.rank5)

        self.assertEqual(self.char.spell_hit_chance + 10, self.char.spell_hit_chance_spell(30451))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(133))
        self.assertEqual(self.char.spell_hit_chance, self.char.spell_hit_chance_spell(116))


@unittest.skip("Not yet implemented")
class TestImprovedArcaneMissiles(unittest.TestCase):
    improved_arcane_missiles_rank1 = 11237
    improved_arcane_missiles_rank2 = 12463
    improved_arcane_missiles_rank3 = 12464
    improved_arcane_missiles_rank4 = 12469
    improved_arcane_missiles_rank5 = 12470
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

    cold_snap_wand = 19130

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_wand_specialization_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.wand_specialization_rank1)
        self.assertEqual(1.13, self.char.wand_dmg_multiplier())

    def test_wand_specialization_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.wand_specialization_rank2)
        self.assertEqual(1.25, self.char.wand_dmg_multiplier())


class TestArcaneConcentration(unittest.TestCase):
    arcane_concentration_rank1 = 11213

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.combat_handler.apply_spell_effect(self.arcane_concentration_rank1)
        for aura in self.char.combat_handler.active_auras:
            aura.proc[2] = 100

    def test_arcane_concentration(self):
        self.assertEqual(30, self.char.spell_resource_cost(133, True))
        self.char.combat_handler.on_spell_impact(133)
        self.assertEqual(0, self.char.spell_resource_cost(133, True))
        self.assertEqual(30, self.char.spell_resource_cost(133, True))


@unittest.skip("Not yet implemented")
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

    arcane_blast = 30451
    fireball_rank1 = 133
    arcane_missiles_rank11_missile = 38703

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.combat_handler.enemy = Enemy()

    def test_arcane_impact_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_impact_rank1)
        self.assertEqual(2.91, self.char.spell_crit_chance_spell(self.arcane_blast))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.arcane_missiles_rank11_missile))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

    def test_arcane_impact_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_impact_rank2)
        self.assertEqual(4.91, self.char.spell_crit_chance_spell(self.arcane_blast))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.arcane_missiles_rank11_missile))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

    def test_arcane_impact_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_impact_rank3)
        self.assertEqual(6.91, self.char.spell_crit_chance_spell(self.arcane_blast))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.arcane_missiles_rank11_missile))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))


@unittest.skip("Not yet implemented")
class TestArcaneFortitude(unittest.TestCase):
    arcane_fortitude_rank1 = 28574

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arcane_fortitude(self):
        self.assertEqual(True, False)


@unittest.skip("Not yet implemented")
class TestImprovedManaShield(unittest.TestCase):
    improved_mana_shield_rank1 = 11252
    improved_mana_shield_rank2 = 12605

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_mana_shield_rank1(self):
        self.assertEqual(True, False)


@unittest.skip("Not yet implemented")
class TestImprovedCounterspell(unittest.TestCase):
    improved_counterspell_rank1 = 11255
    improved_counterspell_rank2 = 12598

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_counterspell_rank1(self):
        self.assertEqual(True, False)


class TestArcaneMeditation(unittest.TestCase):
    arcane_meditation_rank1 = 18462
    arcane_meditation_rank2 = 18463
    arcane_meditation_rank3 = 18464

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spirit = 100
        self.char.intellect = 100

    def test_arcane_meditation_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_meditation_rank1)
        self.assertEqual(round(18.654 * 0.1), self.char.mana_per_tick_while_casting())

    def test_arcane_meditation_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_meditation_rank2)
        self.assertEqual(round(18.654 * 0.2), self.char.mana_per_tick_while_casting())

    def test_arcane_meditation_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_meditation_rank3)
        self.assertEqual(round(18.654 * 0.3), self.char.mana_per_tick_while_casting())


@unittest.skip("Not yet implemented")
class TestImprovedBlink(unittest.TestCase):
    improved_blink_rank1 = 31569
    improved_blink_rank2 = 31570

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_blink_rank1(self):
        self.assertEqual(True, False)


class TestPresenceofMind(unittest.TestCase):
    presence_of_mind = 12043

    pyroblast_rank1 = 11366
    frostbolt_rank1 = 116
    fireball_rank1 = 133

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_presence_of_mind(self):
        self.char.combat_handler.apply_spell_effect(self.presence_of_mind)
        self.assertEqual(0, self.char.spell_cast_time(self.pyroblast_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_cast_time(self.frostbolt_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_cast_time(self.fireball_rank1, proc_auras=True))
        self.assertEqual(1500, self.char.spell_cast_time(self.frostbolt_rank1))


class TestArcaneMind(unittest.TestCase):
    arcane_mind_rank1 = 11232
    arcane_mind_rank2 = 12500
    arcane_mind_rank3 = 12501
    arcane_mind_rank4 = 12502
    arcane_mind_rank5 = 12503

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.intellect = 100

    def test_arcane_mind_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_mind_rank1)
        self.assertEqual(103, self.char.total_intellect)

    def test_arcane_mind_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_mind_rank2)
        self.assertEqual(106, self.char.total_intellect)

    def test_arcane_mind_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_mind_rank3)
        self.assertEqual(109, self.char.total_intellect)

    def test_arcane_mind_rank4(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_mind_rank4)
        self.assertEqual(112, self.char.total_intellect)

    def test_arcane_mind_rank5(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_mind_rank5)
        self.assertEqual(115, self.char.total_intellect)


@unittest.skip("Not yet implemented")
class TestPrismaticCloak(unittest.TestCase):
    prismatic_cloak_rank1 = 31574
    prismatic_cloak_rank2 = 31575

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_prismatic_cloak_rank1(self):
        self.assertEqual(True, False)


class TestArcaneInstability(unittest.TestCase):
    arcane_instability_rank1 = 15058
    arcane_instability_rank2 = 15059
    arcane_instability_rank3 = 15060

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.combat_handler.enemy = Enemy()

    def test_arcane_instability_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_instability_rank1)
        self.assertEqual(1.01, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

        self.assertEqual(1.01, self.char.spell_dmg_multiplier(self.frostbolt_rank1))
        self.assertEqual(1.91, self.char.spell_crit_chance_spell(self.frostbolt_rank1))

    def test_arcane_instability_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_instability_rank2)
        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(2.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.frostbolt_rank1))
        self.assertEqual(2.91, self.char.spell_crit_chance_spell(self.frostbolt_rank1))

    def test_arcane_instability_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_instability_rank3)
        self.assertEqual(1.03, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(3.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

        self.assertEqual(1.03, self.char.spell_dmg_multiplier(self.frostbolt_rank1))
        self.assertEqual(3.91, self.char.spell_crit_chance_spell(self.frostbolt_rank1))


class TestArcanePotency(unittest.TestCase):
    arcane_potency_rank1 = 31571
    arcane_potency_rank2 = 31572
    arcane_potency_rank3 = 31573

    fireball_rank1 = 133

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.combat_handler.enemy = Enemy()

    def test_arcane_potency_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_potency_rank1)
        self.char.combat_handler.apply_spell_effect(12536)
        self.assertEqual(10.91, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

    def test_arcane_potency_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_potency_rank2)
        self.char.combat_handler.apply_spell_effect(12536)
        self.assertEqual(20.91, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))

    def test_arcane_potency_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.arcane_potency_rank3)
        self.char.combat_handler.apply_spell_effect(12536)
        self.assertEqual(30.91, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank1))


class TestEmpoweredArcaneMissiles(unittest.TestCase):
    empowered_arcane_missiles_rank1 = 31579
    empowered_arcane_missiles_rank2 = 31582
    empowered_arcane_missiles_rank3 = 31583

    arcane_missiles_rank1 = 5143
    arcane_missiles_rank1_missile = 7268

    mana_cost_arcane_missiles_rank1 = 85
    fireball_rank1 = 133
    fireball_rank1_mana_cost = 30

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_empowered_arcane_missiles_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.empowered_arcane_missiles_rank1)

        self.assertEqual(round(self.char.combat_handler.spell_power_coefficient(self.arcane_missiles_rank1_missile)
                               + 0.03, 3),
                         self.char.spell_power_coefficient(self.arcane_missiles_rank1_missile))
        self.assertEqual(self.char.combat_handler.spell_power_coefficient(self.fireball_rank1),
                         self.char.spell_power_coefficient(self.fireball_rank1))

        self.assertEqual(round(self.mana_cost_arcane_missiles_rank1 * 1.02),
                         self.char.spell_resource_cost(self.arcane_missiles_rank1))
        self.assertEqual(self.fireball_rank1_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank1))

    def test_empowered_arcane_missiles_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.empowered_arcane_missiles_rank2)

        self.assertEqual(round(self.char.combat_handler.spell_power_coefficient(self.arcane_missiles_rank1_missile)
                               + 0.06, 3),
                         self.char.spell_power_coefficient(self.arcane_missiles_rank1_missile))
        self.assertEqual(self.char.combat_handler.spell_power_coefficient(self.fireball_rank1),
                         self.char.spell_power_coefficient(self.fireball_rank1))

        self.assertEqual(round(self.mana_cost_arcane_missiles_rank1 * 1.04),
                         self.char.spell_resource_cost(self.arcane_missiles_rank1))
        self.assertEqual(self.fireball_rank1_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank1))

    def test_empowered_arcane_missiles_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.empowered_arcane_missiles_rank3)

        self.assertEqual(round(self.char.combat_handler.spell_power_coefficient(self.arcane_missiles_rank1_missile)
                               + 0.09, 3),
                         self.char.spell_power_coefficient(self.arcane_missiles_rank1_missile))
        self.assertEqual(self.char.combat_handler.spell_power_coefficient(self.fireball_rank1),
                         self.char.spell_power_coefficient(self.fireball_rank1))

        self.assertEqual(round(self.mana_cost_arcane_missiles_rank1 * 1.06),
                         self.char.spell_resource_cost(self.arcane_missiles_rank1))
        self.assertEqual(self.fireball_rank1_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank1))


class TestArcanePower(unittest.TestCase):
    arcane_power = 12042

    fireball_rank1 = 133
    fireball_rank1_mana_cost = 30

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.combat_handler.apply_spell_effect(self.arcane_power)

    def test_arcane_power(self):
        self.assertEqual(1.3, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(self.fireball_rank1_mana_cost * 1.3, self.char.spell_resource_cost(self.fireball_rank1))


class TestSpellPower(unittest.TestCase):
    spell_power_rank1 = 35578
    spell_power_rank2 = 35581

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_spell_power_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.spell_power_rank1)

        self.assertEqual(1.75, self.char.spell_crit_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.75, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank1))

    def test_spell_power_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.spell_power_rank2)

        self.assertEqual(2, self.char.spell_crit_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(2, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank1))


class TestMindMastery(unittest.TestCase):
    mind_mastery_rank1 = 31584
    mind_mastery_rank2 = 31585
    mind_mastery_rank3 = 31586
    mind_mastery_rank4 = 31587
    mind_mastery_rank5 = 31588

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.intellect = 100

    def test_mind_mastery_rank1(self):
        self.char.combat_handler.apply_spell_effect(self.mind_mastery_rank1)

        self.assertEqual(5, self.char.total_fire_power)
        self.assertEqual(5, self.char.total_nature_power)
        self.assertEqual(5, self.char.total_frost_power)
        self.assertEqual(5, self.char.total_shadow_power)
        self.assertEqual(5, self.char.total_arcane_power)

    def test_mind_mastery_rank2(self):
        self.char.combat_handler.apply_spell_effect(self.mind_mastery_rank2)

        self.assertEqual(10, self.char.total_fire_power)
        self.assertEqual(10, self.char.total_nature_power)
        self.assertEqual(10, self.char.total_frost_power)
        self.assertEqual(10, self.char.total_shadow_power)
        self.assertEqual(10, self.char.total_arcane_power)

    def test_mind_mastery_rank3(self):
        self.char.combat_handler.apply_spell_effect(self.mind_mastery_rank3)

        self.assertEqual(15, self.char.total_fire_power)
        self.assertEqual(15, self.char.total_nature_power)
        self.assertEqual(15, self.char.total_frost_power)
        self.assertEqual(15, self.char.total_shadow_power)
        self.assertEqual(15, self.char.total_arcane_power)

    def test_mind_mastery_rank4(self):
        self.char.combat_handler.apply_spell_effect(self.mind_mastery_rank4)

        self.assertEqual(20, self.char.total_fire_power)
        self.assertEqual(20, self.char.total_nature_power)
        self.assertEqual(20, self.char.total_frost_power)
        self.assertEqual(20, self.char.total_shadow_power)
        self.assertEqual(20, self.char.total_arcane_power)

    def test_mind_mastery_rank5(self):
        self.char.combat_handler.apply_spell_effect(self.mind_mastery_rank5)

        self.assertEqual(25, self.char.total_fire_power)
        self.assertEqual(25, self.char.total_nature_power)
        self.assertEqual(25, self.char.total_frost_power)
        self.assertEqual(25, self.char.total_shadow_power)
        self.assertEqual(25, self.char.total_arcane_power)


if __name__ == '__main__':
    unittest.main()
