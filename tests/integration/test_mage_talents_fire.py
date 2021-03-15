import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock

import simpy

from src.character import Character as Char
from src.enemy import Enemy
from src.sim_results import SimResult


class TestImprovedFireball(unittest.TestCase):
    improved_fireball_rank1 = 11069
    improved_fireball_rank2 = 12338
    improved_fireball_rank3 = 12339
    improved_fireball_rank4 = 12340
    improved_fireball_rank5 = 12341

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_improved_fireball_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fireball_rank1)

        self.assertEqual(3400, self.char.spell_cast_time(self.fireball_rank14))
        self.assertEqual(3000, self.char.spell_cast_time(self.frostbolt_rank14))

    def test_improved_fireball_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fireball_rank2)

        self.assertEqual(3300, self.char.spell_cast_time(self.fireball_rank14))
        self.assertEqual(3000, self.char.spell_cast_time(self.frostbolt_rank14))

    def test_improved_fireball_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fireball_rank3)

        self.assertEqual(3200, self.char.spell_cast_time(self.fireball_rank14))
        self.assertEqual(3000, self.char.spell_cast_time(self.frostbolt_rank14))

    def test_improved_fireball_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fireball_rank4)

        self.assertEqual(3100, self.char.spell_cast_time(self.fireball_rank14))
        self.assertEqual(3000, self.char.spell_cast_time(self.frostbolt_rank14))

    def test_improved_fireball_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fireball_rank5)

        self.assertEqual(3000, self.char.spell_cast_time(self.fireball_rank14))
        self.assertEqual(3000, self.char.spell_cast_time(self.frostbolt_rank14))


@unittest.skip("Not yet implemented")
class TestImpact(unittest.TestCase):
    impact_rank1 = 11103
    impact_rank2 = 12357
    impact_rank3 = 12358
    impact_rank4 = 12359
    impact_rank5 = 12360

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_impact_rank1(self):
        self.assertEqual(True, False)


my_dot = None


def process(dot):
    global my_dot
    my_dot = dot


def spell_does_hit(spell_id):
    return True


class TestIgnite(unittest.TestCase):
    ignite_rank1 = 11119
    ignite_rank2 = 11120
    ignite_rank3 = 12846
    ignite_rank4 = 12847
    ignite_rank5 = 12848

    sim_length = 5000

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697
    crit_damage = 12800

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.results = SimResult(sim_length=self.sim_length, start_time=datetime.now())
        self.char.spell_handler.env = simpy.Environment()
        self.char.spell_handler.spell_does_hit = Mock(side_effect=spell_does_hit)

    def test_ignite_fire_damage_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank1)
        self.char.spell_handler.on_spell_crit(self.fireball_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == 12654 and spell_cast.dot_damage_dealt == round(self.crit_damage * 0.08 / 3) * 3
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))

    def test_ignite_fire_damage_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank2)
        self.char.spell_handler.on_spell_crit(self.fireball_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == 12654 and spell_cast.dot_damage_dealt == round(self.crit_damage * 0.16 / 3) * 3
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))

    def test_ignite_fire_damage_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank3)
        self.char.spell_handler.on_spell_crit(self.fireball_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == 12654 and spell_cast.dot_damage_dealt == round(self.crit_damage * 0.24 / 3) * 3
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))

    def test_ignite_fire_damage_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank4)
        self.char.spell_handler.on_spell_crit(self.fireball_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == 12654 and spell_cast.dot_damage_dealt == round(self.crit_damage * 0.32 / 3) * 3
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))

    def test_ignite_fire_damage_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank5)
        self.char.spell_handler.on_spell_crit(self.fireball_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == 12654 and spell_cast.dot_damage_dealt == round(self.crit_damage * 0.4 / 3) * 3
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))

    def test_ignite_doesnt_proc_on_frost(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank5)
        self.char.spell_handler.on_spell_crit(self.frostbolt_rank14, self.crit_damage)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertFalse(any(spell_cast.spell_id == 12654 for
                             spell_cast in self.char.spell_handler.results.cast_spells.values()))


@unittest.skip("Not yet implemented")
class TestFlameThrowing(unittest.TestCase):
    flame_throwing_rank1 = 11100
    flame_throwing_rank2 = 12353

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_flame_throwing_rank1(self):
        self.assertEqual(True, False)


class TestImprovedFireBlast(unittest.TestCase):
    improved_fire_blast_rank1 = 11078
    improved_fire_blast_rank2 = 11080
    improved_fire_blast_rank3 = 12342

    fire_blast_rank9 = 27079
    cone_of_cold_rank1 = 120

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.results = Mock()
        self.char.spell_handler.damage_spell_hit = MagicMock()
        self.char.spell_handler.env.now = 0

    def test_improved_fire_blast_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fire_blast_rank1)
        self.char.spell_handler.spell_start_cooldown(self.fire_blast_rank9)
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)

        self.assertEqual(7500, self.char.spell_handler.cooldown_family_mask[2][0])
        self.assertEqual(10000, self.char.spell_handler.cooldown_family_mask[1573376][0])

    def test_improved_fire_blast_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fire_blast_rank2)
        self.char.spell_handler.spell_start_cooldown(self.fire_blast_rank9)
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)

        self.assertEqual(7000, self.char.spell_handler.cooldown_family_mask[2][0])
        self.assertEqual(10000, self.char.spell_handler.cooldown_family_mask[1573376][0])

    def test_improved_fire_blast_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_fire_blast_rank3)
        self.char.spell_handler.spell_start_cooldown(self.fire_blast_rank9)
        self.char.spell_handler.spell_start_cooldown(self.cone_of_cold_rank1)

        self.assertEqual(6500, self.char.spell_handler.cooldown_family_mask[2][0])
        self.assertEqual(10000, self.char.spell_handler.cooldown_family_mask[1573376][0])


class TestIncineration(unittest.TestCase):
    incineration_rank1 = 18459
    incineration_rank2 = 18460

    fire_blast_rank9 = 27079
    scorch_rank9 = 27074
    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()

    def test_incineration_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.incineration_rank1)

        self.assertEqual(2, self.char.spell_crit_chance_spell(self.fire_blast_rank9))
        self.assertEqual(2, self.char.spell_crit_chance_spell(self.scorch_rank9))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1))

    def test_incineration_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.incineration_rank2)

        self.assertEqual(4, self.char.spell_crit_chance_spell(self.fire_blast_rank9))
        self.assertEqual(4, self.char.spell_crit_chance_spell(self.scorch_rank9))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1))


class TestImprovedFlamestrike(unittest.TestCase):
    improved_flamestrike_rank1 = 11108
    improved_flamestrike_rank2 = 12349
    improved_flamestrike_rank3 = 12350

    flamestrike_rank1 = 2120
    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()

    def test_improved_flamestrike_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_flamestrike_rank1)

        self.assertEqual(5, self.char.spell_crit_chance_spell(self.flamestrike_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1, proc_auras=False))

    def test_improved_flamestrike_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_flamestrike_rank2)

        self.assertEqual(10, self.char.spell_crit_chance_spell(self.flamestrike_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1, proc_auras=False))

    def test_improved_flamestrike_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_flamestrike_rank3)

        self.assertEqual(15, self.char.spell_crit_chance_spell(self.flamestrike_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank1, proc_auras=False))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1, proc_auras=False))


class TestPyroblast(unittest.TestCase):
    pyroblast_rank1 = 11366
    sim_length = 13000

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.results = SimResult(sim_length=self.sim_length, start_time=datetime.now())
        self.char.spell_handler.env = simpy.Environment()
        self.char.spell_handler.spell_does_hit = Mock(side_effect=spell_does_hit)

    def test_pyroblast_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.pyroblast_rank1)

        for i in range(1, self.sim_length):
            self.char.spell_handler.env.run(until=i)

        self.assertTrue(
            any(spell_cast.spell_id == self.pyroblast_rank1 and
                spell_cast.damage_dealt != 0 and spell_cast.dot_damage_dealt != 0
                for spell_cast in self.char.spell_handler.results.cast_spells.values()))


@unittest.skip("Not yet implemented")
class TestBurningSoul(unittest.TestCase):
    burning_soul_rank1 = 11083
    burning_soul_rank2 = 12351

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_burning_soul_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.burning_soul_rank1)

        self.assertEqual(True, False)


class TestImprovedScorch(unittest.TestCase):
    improved_scorch_rank1 = 11095
    improved_scorch_rank2 = 12872
    improved_scorch_rank3 = 12873

    scorch_rank9 = 27074
    frostbolt_rank1 = 116
    fireball_rank1 = 133

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0

    def test_improved_scorch_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.improved_scorch_rank1)
        self.assertEqual(33, self.char.spell_handler.active_auras[0].value)

    def test_improved_scorch_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.improved_scorch_rank2)
        self.assertEqual(66, self.char.spell_handler.active_auras[0].value)

    def test_improved_scorch_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.improved_scorch_rank3)
        self.assertEqual(100, self.char.spell_handler.active_auras[0].value)

    def test_improved_scorch_stack_application(self):
        self.char.spell_handler.apply_spell_effect(self.improved_scorch_rank3)
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 for aura in self.char.spell_handler.enemy.active_auras))
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 1
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 2
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 3
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.fireball_rank1)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 3
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 4
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 5
                            for aura in self.char.spell_handler.enemy.active_auras))
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertTrue(any(aura.spell_id == 22959 and aura.curr_stacks == 5
                            for aura in self.char.spell_handler.enemy.active_auras))

    def test_improved_scorch_effect(self):
        self.char.spell_handler.apply_spell_effect(self.improved_scorch_rank3)
        self.char.spell_handler.on_spell_hit(self.scorch_rank9)
        self.assertEqual(1.03, self.char.spell_handler.enemy_damage_taken_mod(self.scorch_rank9))
        self.assertEqual(1.03, self.char.spell_handler.enemy_damage_taken_mod(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_handler.enemy_damage_taken_mod(self.frostbolt_rank1))


@unittest.skip("Not yet implemented")
class TestMoltenShields(unittest.TestCase):
    molten_shields_rank1 = 11094
    molten_shields_rank2 = 12043

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_molten_shields_rank1(self):
        self.assertEqual(True, False)


class TestMasterofElements(unittest.TestCase):
    master_of_elements_rank1 = 29074
    master_of_elements_rank2 = 29075
    master_of_elements_rank3 = 29076

    fireball_rank1 = 133
    fireball_rank1_mana_cost = 30

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.intellect = 3000
        self.char.current_mana = 200

    def test_master_of_elements_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.master_of_elements_rank1)
        self.char.spell_handler.on_spell_crit(self.fireball_rank1)
        self.assertEqual(203, self.char.current_mana)

    def test_master_of_elements_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.master_of_elements_rank2)
        self.char.spell_handler.on_spell_crit(self.fireball_rank1)
        self.assertEqual(206, self.char.current_mana)

    def test_master_of_elements_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.master_of_elements_rank3)
        self.char.spell_handler.on_spell_crit(self.fireball_rank1)
        self.assertEqual(209, self.char.current_mana)


class TestPlayingWithFire(unittest.TestCase):
    playing_with_fire_rank1 = 31638
    playing_with_fire_rank2 = 31639
    playing_with_fire_rank3 = 31640

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_playing_with_fire_rank1_damage_caused(self):
        self.char.spell_handler.apply_spell_effect(self.playing_with_fire_rank1)
        self.assertEqual(1.01, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.01, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_playing_with_fire_rank2_damage_caused(self):
        self.char.spell_handler.apply_spell_effect(self.playing_with_fire_rank2)
        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_playing_with_fire_rank3_damage_caused(self):
        self.char.spell_handler.apply_spell_effect(self.playing_with_fire_rank3)
        self.assertEqual(1.03, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.03, self.char.spell_dmg_multiplier(self.frostbolt_rank1))


class TestCriticalMass(unittest.TestCase):
    critical_mass_rank1 = 11115
    critical_mass_rank2 = 11367
    critical_mass_rank3 = 11368

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()

    def test_critical_mass_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.critical_mass_rank1)
        self.assertEqual(2, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1))

    def test_critical_mass_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.critical_mass_rank2)
        self.assertEqual(4, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1))

    def test_critical_mass_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.critical_mass_rank3)
        self.assertEqual(6, self.char.spell_crit_chance_spell(self.fireball_rank1))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank1))


@unittest.skip("Not yet implemented")
class TestBlastWave(unittest.TestCase):
    pass


@unittest.skip("Not yet implemented")
class TestBlazingSpeed(unittest.TestCase):
    pass


class TestFirePower(unittest.TestCase):
    fire_power_rank1 = 11124
    fire_power_rank2 = 12378
    fire_power_rank3 = 12398
    fire_power_rank4 = 12399
    fire_power_rank5 = 12400

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_fire_power_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.fire_power_rank1)
        self.assertEqual(1.02, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_fire_power_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.fire_power_rank2)
        self.assertEqual(1.04, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_fire_power_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.fire_power_rank3)
        self.assertEqual(1.06, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_fire_power_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.fire_power_rank4)
        self.assertEqual(1.08, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_fire_power_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.fire_power_rank5)
        self.assertEqual(1.1, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))


class TestPyromaniac(unittest.TestCase):
    pyromaniac_rank1 = 34293
    pyromaniac_rank2 = 34295
    pyromaniac_rank3 = 34296

    fireball_rank14 = 38692
    fireball_rank14_mana_cost = 465

    frostbolt_rank14 = 38697
    frostbolt_rank14_mana_cost = 345

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Enemy()

    def test_pyromaniac_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.pyromaniac_rank1)
        self.assertEqual(1, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.99),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(self.frostbolt_rank14_mana_cost, self.char.spell_resource_cost(self.frostbolt_rank14))

    def test_pyromaniac_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.pyromaniac_rank2)
        self.assertEqual(2, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.98),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(self.frostbolt_rank14_mana_cost, self.char.spell_resource_cost(self.frostbolt_rank14))

    def test_pyromaniac_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.pyromaniac_rank3)
        self.assertEqual(3, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.assertEqual(round(self.fireball_rank14_mana_cost * 0.97),
                         self.char.spell_resource_cost(self.fireball_rank14))
        self.assertEqual(self.frostbolt_rank14_mana_cost, self.char.spell_resource_cost(self.frostbolt_rank14))


# TODO only start cooldown after all charges used
class TestCombustion(unittest.TestCase):
    combustion = 11129

    fireball_rank14 = 38692
    fireball_rank14_mana_cost = 465

    frostbolt_rank14 = 38697
    frostbolt_rank14_mana_cost = 345

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.now = 0
        self.char.spell_handler.enemy = Enemy()

    def test_combustion(self):
        self.char.spell_handler.apply_spell_effect(self.combustion)
        self.assertEqual(10, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_hit(self.fireball_rank14)
        self.assertEqual(20, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_hit(self.frostbolt_rank14)
        self.assertEqual(20, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_crit(self.fireball_rank14)
        self.assertEqual(30, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_crit(self.fireball_rank14)
        self.assertEqual(40, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_hit(self.fireball_rank14)
        self.assertEqual(50, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_crit(self.frostbolt_rank14)
        self.assertEqual(50, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))

        self.char.spell_handler.on_spell_crit(self.fireball_rank14)
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.fireball_rank14))
        self.assertEqual(0, self.char.spell_crit_chance_spell(self.frostbolt_rank14))


class TestMoltenFury(unittest.TestCase):
    molten_fury_rank1 = 31679
    molten_fury_rank2 = 31680

    fireball_rank1 = 133
    frostbolt_rank1 = 116

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.enemy = Mock()
        self.char.spell_handler.enemy.in_execute_range = False

    def test_molten_fury_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.molten_fury_rank1)
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

        self.char.spell_handler.enemy.in_execute_range = True
        self.assertEqual(1.1, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))

    def test_molten_fury_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.molten_fury_rank2)
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1, self.char.spell_dmg_multiplier(self.frostbolt_rank1))
        self.char.spell_handler.enemy.in_execute_range = True
        self.assertEqual(1.2, self.char.spell_dmg_multiplier(self.fireball_rank1))
        self.assertEqual(1.2, self.char.spell_dmg_multiplier(self.frostbolt_rank1))


class TestEmpoweredFireball(unittest.TestCase):
    empowered_fireball_rank1 = 31656
    empowered_fireball_rank2 = 31657
    empowered_fireball_rank3 = 31658
    empowered_fireball_rank4 = 31659
    empowered_fireball_rank5 = 31660

    fireball_rank14 = 38692
    frostbolt_rank14 = 38697

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"

    def test_empowered_fireball_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_fireball_rank1)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14) + 0.03,
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14),
                         self.char.spell_power_coefficient(self.frostbolt_rank14))

    def test_empowered_fireball_rank2(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_fireball_rank2)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14) + 0.06,
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14),
                         self.char.spell_power_coefficient(self.frostbolt_rank14))

    def test_empowered_fireball_rank3(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_fireball_rank3)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14) + 0.09,
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14),
                         self.char.spell_power_coefficient(self.frostbolt_rank14))

    def test_empowered_fireball_rank4(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_fireball_rank4)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14) + 0.12,
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14),
                         self.char.spell_power_coefficient(self.frostbolt_rank14))

    def test_empowered_fireball_rank5(self):
        self.char.spell_handler.apply_spell_effect(self.empowered_fireball_rank5)
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.fireball_rank14) + 0.15,
                         self.char.spell_power_coefficient(self.fireball_rank14))
        self.assertEqual(self.char.spell_handler.spell_power_coefficient(self.frostbolt_rank14),
                         self.char.spell_power_coefficient(self.frostbolt_rank14))


@unittest.skip("Not yet implemented")
class TestDragonsBreath(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
