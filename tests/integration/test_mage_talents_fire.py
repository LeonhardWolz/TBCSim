import unittest
from unittest.mock import MagicMock, Mock

from src.character import Character as Char


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

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.spell_handler.env = Mock()
        self.char.spell_handler.env.process = Mock(side_effect=process)
        self.char.spell_handler.spell_does_hit = Mock(side_effect=spell_does_hit)

    def test_ignite_rank1(self):
        self.char.spell_handler.apply_spell_effect(self.ignite_rank1)
        self.char.spell_handler.process_on_spell_crit(38692, 100)
        print(dir(my_dot))
        self.assertEqual(8, my_dot)


if __name__ == '__main__':
    unittest.main()
