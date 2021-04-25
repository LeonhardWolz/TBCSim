import unittest
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.sim.sim_objects.character import Character as Char
from src.sim.sim_objects.enemy import Enemy
from src.sim.results.sim_results import SimResult


@unittest.skip("Not yet implemented")
class TestFrostWarding(unittest.TestCase):
    frost_warding_rank1 = 11189
    frost_warding_rank2 = 28332

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"


class TestImprovedFrostbolt(unittest.TestCase):
    improved_frostbolt_rank1 = 11070
    improved_frostbolt_rank2 = 12473
    improved_frostbolt_rank3 = 16763
    improved_frostbolt_rank4 = 16765
    improved_frostbolt_rank5 = 16766

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_frostbolt_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frostbolt_rank1)
        self.assertEqual(2900, self.char.spell_cast_time(self.frostbolt_rank14))
        self.assertEqual(3500, self.char.spell_cast_time(self.fireball_rank14))

    def test_improved_frostbolt_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frostbolt_rank2)
        self.assertEqual(2800, self.char.spell_cast_time(self.frostbolt_rank14))
        self.assertEqual(3500, self.char.spell_cast_time(self.fireball_rank14))

    def test_improved_frostbolt_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frostbolt_rank3)
        self.assertEqual(2700, self.char.spell_cast_time(self.frostbolt_rank14))
        self.assertEqual(3500, self.char.spell_cast_time(self.fireball_rank14))

    def test_improved_frostbolt_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frostbolt_rank4)
        self.assertEqual(2600, self.char.spell_cast_time(self.frostbolt_rank14))
        self.assertEqual(3500, self.char.spell_cast_time(self.fireball_rank14))

    def test_improved_frostbolt_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frostbolt_rank5)
        self.assertEqual(2500, self.char.spell_cast_time(self.frostbolt_rank14))
        self.assertEqual(3500, self.char.spell_cast_time(self.fireball_rank14))


class TestElementalPrecision(unittest.TestCase):
    elemental_precision_rank1 = 29438
    elemental_precision_rank2 = 29439
    elemental_precision_rank3 = 29440

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697
    arcane_blast_rank1 = 30451

    fireball_rank14_mana_cost = 465
    frostbolt_rank14_mana_cost = 345
    arcane_blast_rank1_mana_cost = 195

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_elemental_precision_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.elemental_precision_rank1)
        self.assertEqual(1, self.char.spell_hit_chance_spell(self.fireball_rank14))
        self.assertEqual(1, self.char.spell_hit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0, self.char.spell_hit_chance_spell(self.arcane_blast_rank1))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.99),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.99),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.arcane_blast_rank1_mana_cost,
                         self.char.spell_resource_cost(self.arcane_blast_rank1))

    def test_elemental_precision_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.elemental_precision_rank2)
        self.assertEqual(2, self.char.spell_hit_chance_spell(self.fireball_rank14))
        self.assertEqual(2, self.char.spell_hit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0, self.char.spell_hit_chance_spell(self.arcane_blast_rank1))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.98),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.98),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.arcane_blast_rank1_mana_cost,
                         self.char.spell_resource_cost(self.arcane_blast_rank1))

    def test_elemental_precision_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.elemental_precision_rank3)
        self.assertEqual(3, self.char.spell_hit_chance_spell(self.fireball_rank14))
        self.assertEqual(3, self.char.spell_hit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0, self.char.spell_hit_chance_spell(self.arcane_blast_rank1))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.97),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.97),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.arcane_blast_rank1_mana_cost,
                         self.char.spell_resource_cost(self.arcane_blast_rank1))


class TestIceShards(unittest.TestCase):
    ice_shards_rank1 = 11207
    ice_shards_rank2 = 12672
    ice_shards_rank3 = 15047
    ice_shards_rank4 = 15052
    ice_shards_rank5 = 15053

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_ice_shards_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.ice_shards_rank1)
        self.assertEqual(1.50 * 1.2, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1.50, self.char.spell_crit_dmg_multiplier(self.fireball_rank14))

    def test_ice_shards_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.ice_shards_rank2)
        self.assertEqual(1.50 * 1.4, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1.50, self.char.spell_crit_dmg_multiplier(self.fireball_rank14))

    def test_ice_shards_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.ice_shards_rank3)
        self.assertEqual(1.50 * 1.6, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1.50, self.char.spell_crit_dmg_multiplier(self.fireball_rank14))

    def test_ice_shards_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.ice_shards_rank4)
        self.assertEqual(1.50 * 1.8, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1.50, self.char.spell_crit_dmg_multiplier(self.fireball_rank14))

    def test_ice_shards_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.ice_shards_rank5)
        self.assertEqual(1.50 * 2, self.char.spell_crit_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1.50, self.char.spell_crit_dmg_multiplier(self.fireball_rank14))


class TestFrostbite(unittest.TestCase):
    frostbite_rank1 = 11071
    frostbite_rank2 = 12496
    frostbite_rank3 = 12497

    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0
        self.char.spell_handler.results = Mock()
        self.char.spell_handler.results.damage_spell_hit = MagicMock()

    def test_frostbite_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.frostbite_rank1)
        self.assertTrue(any(aura.spell_id == 11071 and aura.value == 5
                            for aura in self.char.spell_handler.active_auras))

    def test_frostbite_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.frostbite_rank2)
        self.assertTrue(any(aura.spell_id == 12496 and aura.value == 10
                            for aura in self.char.spell_handler.active_auras))

    def test_frostbite_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.frostbite_rank3)
        self.assertTrue(any(aura.spell_id == 12497 and aura.value == 15
                            for aura in self.char.spell_handler.active_auras))

    def test_frostbite_application(self):
        self.char.spell_handler.apply_spell_effect(self.frostbite_rank3)
        for aura in self.char.spell_handler.active_auras:
            if aura.spell_id == 12497:
                aura.value = 100
        self.char.spell_handler.apply_spell_effect(self.frostbolt_rank14)

        self.assertTrue(any(aura.spell_id == 12494 for aura in self.char.spell_handler.enemy.active_auras))


class TestImprovedFrostNova(unittest.TestCase):
    improved_frost_nova_rank1 = 11165
    improved_frost_nova_rank2 = 12475

    frost_nova_rank5 = 27088
    ice_barrier_rank6 = 33405

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0

    def test_improved_frost_nova_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frost_nova_rank1)
        self.char.spell_handler.spell_start_cooldown(self.frost_nova_rank5)
        self.char.spell_handler.spell_start_cooldown(self.ice_barrier_rank6)

        self.assertEqual(23000, self.char.spell_handler.cooldown_spell_family_mask[524352][0])
        self.assertEqual(30000, self.char.spell_handler.cooldown_spell_family_mask[4294967296][0])

    def test_improved_frost_nova_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_frost_nova_rank2)
        self.char.spell_handler.spell_start_cooldown(self.frost_nova_rank5)
        self.char.spell_handler.spell_start_cooldown(self.ice_barrier_rank6)

        self.assertEqual(21000, self.char.spell_handler.cooldown_spell_family_mask[524352][0])
        self.assertEqual(30000, self.char.spell_handler.cooldown_spell_family_mask[4294967296][0])


@unittest.skip("Not yet implemented")
class TestPermafrost(unittest.TestCase):
    permafrost_rank1 = 11175
    permafrost_rank2 = 12569
    permafrost_rank3 = 12571

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"


class TestPiercingIce(unittest.TestCase):
    piercing_ice_rank1 = 11151
    piercing_ice_rank2 = 12952
    piercing_ice_rank3 = 12953
    piercing_ice_rank4 = 12954
    piercing_ice_rank5 = 12957

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_piercing_ice_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.piercing_ice_rank1)
        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_piercing_ice_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.piercing_ice_rank2)
        self.assertEqual(1.04, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_piercing_ice_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.piercing_ice_rank3)
        self.assertEqual(1.06, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_piercing_ice_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.piercing_ice_rank4)
        self.assertEqual(1.08, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_piercing_ice_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.piercing_ice_rank5)
        self.assertEqual(1.1, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))


class TestIcyVeins(unittest.TestCase):
    icy_veins = 12472

    fireball_rank14 = 38692

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_icy_veins(self):
        self.char.spell_handler.apply_spell_effect(self.icy_veins)
        self.assertEqual(self.char.spell_handler.spell_cast_time(self.fireball_rank14) * 0.8,
                         self.char.spell_cast_time(self.fireball_rank14))


@unittest.skip("Not yet implemented")
class TestImprovedBlizzard(unittest.TestCase):
    improved_blizzard_rank1 = 11185
    improved_blizzard_rank2 = 12487
    improved_blizzard_rank3 = 12488

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"


@unittest.skip("Not yet implemented")
class TestArcticReach(unittest.TestCase):
    arctic_reach_rank1 = 16757
    arctic_reach_rank2 = 16758

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"


class TestFrostChanneling(unittest.TestCase):
    frost_channeling_rank1 = 11160
    frost_channeling_rank2 = 12518
    frost_channeling_rank3 = 12519

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    fireball_rank14_mana_cost = 465
    frostbolt_rank14_mana_cost = 345

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_frost_channeling_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.frost_channeling_rank1)
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.95),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.fireball_rank14_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank14))

    def test_frost_channeling_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.frost_channeling_rank2)
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.90),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.fireball_rank14_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank14))

    def test_frost_channeling_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.frost_channeling_rank3)
        self.assertEqual(round(self.frostbolt_rank14_mana_cost * 0.85),
                         self.char.spell_resource_cost(self.frostbolt_rank14))
        self.assertEqual(self.fireball_rank14_mana_cost,
                         self.char.spell_resource_cost(self.fireball_rank14))


class TestShatter(unittest.TestCase):
    shatter_rank1 = 11170
    shatter_rank2 = 12982
    shatter_rank3 = 12983
    shatter_rank4 = 12984
    shatter_rank5 = 12985

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0
        self.char.spell_handler.results = SimResult(start_time=datetime.now(), sim_length=6000)

    def test_shatter_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.shatter_rank1)
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(12494)
        self.assertEqual(10.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(10.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

    def test_shatter_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.shatter_rank2)
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(12494)
        self.assertEqual(20.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(20.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

    def test_shatter_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.shatter_rank3)
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(12494)
        self.assertEqual(30.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(30.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

    def test_shatter_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.shatter_rank4)
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(12494)
        self.assertEqual(40.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(40.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

    def test_shatter_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.shatter_rank5)
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))

        self.char.spell_handler.apply_spell_effect(12494)
        self.assertEqual(50.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14, proc_auras=False))
        self.assertEqual(50.91, self.char.spell_crit_chance_spell(self.fireball_rank14, proc_auras=False))


@unittest.skip("Not yet implemented")
class TestFrozenCore(unittest.TestCase):
    frozen_core_rank1 = 31667
    frozen_core_rank2 = 31668
    frozen_core_rank3 = 31669

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"


class TestColdSnap(unittest.TestCase):
    cold_snap = 11958

    cone_of_cold_rank1 = 120
    ice_barrier_rank1 = 11426
    ice_block = 45438
    frost_nova_rank5 = 27088

    fire_blast_rank9 = 27079

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0

    def test_cold_snap(self):
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_barrier_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_block)
        self.char.spell_handler.spell_start_cooldown(self.frost_nova_rank5)
        self.char.spell_handler.spell_start_cooldown(self.fire_blast_rank9)

        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.cone_of_cold_rank1))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.ice_barrier_rank1))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.ice_block))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.frost_nova_rank5))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.fire_blast_rank9))

        self.char.spell_handler.apply_spell_effect(self.cold_snap)

        self.assertFalse(self.char.spell_handler.spell_on_cooldown(self.cone_of_cold_rank1))
        self.assertFalse(self.char.spell_handler.spell_on_cooldown(self.ice_barrier_rank1))
        self.assertFalse(self.char.spell_handler.spell_on_cooldown(self.ice_block))
        self.assertFalse(self.char.spell_handler.spell_on_cooldown(self.frost_nova_rank5))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.fire_blast_rank9))
        self.assertTrue(self.char.spell_handler.spell_on_cooldown(self.cold_snap))


class TestImprovedConeOfCold(unittest.TestCase):
    improved_cone_of_cold_rank1 = 11190
    improved_cone_of_cold_rank2 = 12489
    improved_cone_of_cold_rank3 = 12490

    cone_of_cold_rank1 = 120
    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_cone_of_cold_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_cone_of_cold_rank1)
        self.assertEqual(1.15, self.char.spell_dmg_multiplier(self.cone_of_cold_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_improved_cone_of_cold_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_cone_of_cold_rank2)
        self.assertEqual(1.25, self.char.spell_dmg_multiplier(self.cone_of_cold_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_improved_cone_of_cold_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_cone_of_cold_rank3)
        self.assertEqual(1.35, self.char.spell_dmg_multiplier(self.cone_of_cold_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))


class TestIceFloes(unittest.TestCase):
    ice_floes_rank1 = 31670
    ice_floes_rank2 = 31672

    cone_of_cold_rank1 = 120
    cold_snap = 11958
    ice_barrier_rank1 = 11426
    ice_block = 45438
    frost_nova_rank5 = 27088

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0

    def test_ice_floes_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.ice_floes_rank1)

        self.char.spell_handler.spell_start_cooldown(self.cold_snap)
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_barrier_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_block)
        self.char.spell_handler.spell_start_cooldown(self.frost_nova_rank5)

        self.assertEqual(480000 * 0.9, self.char.spell_handler.cooldown_spell_id[self.cold_snap][0])
        self.assertEqual(10000 * 0.9, self.char.spell_handler.cooldown_spell_family_mask[1573376][0])
        self.assertEqual(30000 * 0.9, self.char.spell_handler.cooldown_spell_family_mask[4294967296][0])
        self.assertEqual(300000 * 0.9, self.char.spell_handler.cooldown_spell_family_mask[554050781184][0])
        self.assertEqual(25000, self.char.spell_handler.cooldown_spell_family_mask[524352][0])

    def test_ice_floes_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.ice_floes_rank2)

        self.char.spell_handler.spell_start_cooldown(self.cold_snap)
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_barrier_rank1)
        self.char.spell_handler.spell_start_cooldown(self.ice_block)
        self.char.spell_handler.spell_start_cooldown(self.frost_nova_rank5)

        self.assertEqual(480000 * 0.8, self.char.spell_handler.cooldown_spell_id[self.cold_snap][0])
        self.assertEqual(10000 * 0.8, self.char.spell_handler.cooldown_spell_family_mask[1573376][0])
        self.assertEqual(30000 * 0.8, self.char.spell_handler.cooldown_spell_family_mask[4294967296][0])
        self.assertEqual(300000 * 0.8, self.char.spell_handler.cooldown_spell_family_mask[554050781184][0])
        self.assertEqual(25000, self.char.spell_handler.cooldown_spell_family_mask[524352][0])


def spell_does_hit(spell_id):
    return True


class TestWintersChill(unittest.TestCase):
    winters_chill_rank1 = 11180
    winters_chill_rank2 = 28592
    winters_chill_rank3 = 28593
    winters_chill_rank4 = 28594
    winters_chill_rank5 = 28595

    cone_of_cold_rank1 = 120
    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_hit_rating = 2000
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0
        self.char.spell_handler.results = Mock()
        self.char.spell_handler.results.damage_spell_hit = MagicMock()
        self.char.spell_handler.spell_does_hit = Mock(side_effect=spell_does_hit)

    def test_winters_chill_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank1)
        self.assertTrue(any(aura.spell_id == self.winters_chill_rank1 and aura.proc[1] == 20
                            for aura in self.char.spell_handler.active_auras))

    def test_winters_chill_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank2)
        self.assertTrue(any(aura.spell_id == self.winters_chill_rank2 and aura.proc[1] == 40
                            for aura in self.char.spell_handler.active_auras))

    def test_winters_chill_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank3)
        self.assertTrue(any(aura.spell_id == self.winters_chill_rank3 and aura.proc[1] == 60
                            for aura in self.char.spell_handler.active_auras))

    def test_winters_chill_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank4)
        self.assertTrue(any(aura.spell_id == self.winters_chill_rank4 and aura.proc[1] == 80
                            for aura in self.char.spell_handler.active_auras))

    def test_winters_chill_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank5)
        self.assertTrue(any(aura.spell_id == self.winters_chill_rank5 and aura.proc[1] == 100
                            for aura in self.char.spell_handler.active_auras))

    def test_winters_chill_application(self):
        self.char.spell_handler.apply_spell_effect(self.winters_chill_rank5)

        self.char.spell_handler.apply_spell_effect(self.fireball_rank14)
        self.assertFalse(any(aura.spell_id == 12579 for aura in self.char.spell_handler.enemy.active_auras))

        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))

        self.char.spell_handler.apply_spell_effect(self.frostbolt_rank14)
        self.assertTrue(any(aura.spell_id == 12579 for aura in self.char.spell_handler.enemy.active_auras))

        self.assertEqual(2.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))


@unittest.skip("Not yet implemented")
class TestIceBarrier(unittest.TestCase):
    ice_barrier_rank1 = 11426

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_ice_barrier(self):
        self.assertTrue(False)


class TestArcticWinds(unittest.TestCase):
    arctic_winds_rank1 = 31674
    arctic_winds_rank2 = 31675
    arctic_winds_rank3 = 31676
    arctic_winds_rank4 = 31677
    arctic_winds_rank5 = 31678

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_arctic_winds_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.arctic_winds_rank1)

        self.assertEqual(1.01, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_arctic_winds_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.arctic_winds_rank2)

        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_arctic_winds_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.arctic_winds_rank3)

        self.assertEqual(1.03, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_arctic_winds_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.arctic_winds_rank4)

        self.assertEqual(1.04, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))

    def test_arctic_winds_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.arctic_winds_rank5)

        self.assertEqual(1.05, self.char.spell_dmg_multiplier(self.frostbolt_rank14))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank14))


class TestEmpoweredFrostbolt(unittest.TestCase):
    empowered_frostbolt_rank1 = 31682
    empowered_frostbolt_rank2 = 31683
    empowered_frostbolt_rank3 = 31684
    empowered_frostbolt_rank4 = 31685
    empowered_frostbolt_rank5 = 31686

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()

    def test_empowered_frostbolt_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_frostbolt_rank1)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14) + 0.02,
                         self.char.spell_power_coefficient(self.frostbolt_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14),
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(1.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))

    def test_empowered_frostbolt_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_frostbolt_rank2)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14) + 0.04,
                         self.char.spell_power_coefficient(self.frostbolt_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14),
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(2.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))

    def test_empowered_frostbolt_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_frostbolt_rank3)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14) + 0.06,
                         self.char.spell_power_coefficient(self.frostbolt_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14),
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(3.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))

    def test_empowered_frostbolt_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_frostbolt_rank4)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14) + 0.08,
                         self.char.spell_power_coefficient(self.frostbolt_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14),
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(4.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))

    def test_empowered_frostbolt_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_frostbolt_rank5)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14) + 0.1,
                         self.char.spell_power_coefficient(self.frostbolt_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14),
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(5.91, self.char.spell_crit_chance_spell(self.frostbolt_rank14))
        self.assertEqual(0.91, self.char.spell_crit_chance_spell(self.fireball_rank14))


@unittest.skip("Not yet implemented")
class TestSummonWaterElemental(unittest.TestCase):
    summon_water_elemental = 31687

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_summon_water_elemental(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
