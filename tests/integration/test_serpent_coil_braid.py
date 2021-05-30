import unittest
from unittest.mock import Mock

from src.sim.sim_objects.character import Character as Char
import src.db.sqlite_db_connector as DB


class TestSerpentCoilBraid(unittest.TestCase):
    serpent_coil_braid_spell = 37447

    super_mana_potion = 22832
    mana_emerald = 22044
    mana_ruby = 8008

    mana_emerald_spell = 27103
    mana_ruby_spell = 10058
    super_mana_potion_spell = 28499

    def setUp(self) -> None:
        self.char = Char()
        self.char.player_class = "Mage"
        self.char.mana = 10000
        self.char.current_mana = 0
        self.char.combat_handler.results = Mock()
        self.char.combat_handler.env = Mock()
        self.char.combat_handler.env.now = 0

        self.char.active_consumables[self.super_mana_potion] = 0
        self.char.active_consumables[self.mana_emerald] = 0
        self.char.active_consumables[self.mana_ruby] = 0

        self.mana_emerald_spell_info = list(DB.get_spell(self.mana_emerald_spell))
        self.mana_emerald_spell_info[DB.spell_column_info["EffectBasePoints1"]] = 1999
        self.mana_emerald_spell_info[DB.spell_column_info["EffectDieSides1"]] = 1
        self.mana_emerald_spell_info[DB.spell_column_info["EffectBaseDice1"]] = 1
        self.mana_emerald_spell_info = tuple(self.mana_emerald_spell_info)

        self.mana_ruby_spell_info = list(DB.get_spell(self.mana_ruby_spell))
        self.mana_ruby_spell_info[DB.spell_column_info["EffectBasePoints1"]] = 1999
        self.mana_ruby_spell_info[DB.spell_column_info["EffectDieSides1"]] = 1
        self.mana_ruby_spell_info[DB.spell_column_info["EffectBaseDice1"]] = 1
        self.mana_ruby_spell_info = tuple(self.mana_ruby_spell_info)

        self.super_mana_potion_spell_info = list(DB.get_spell(self.super_mana_potion_spell))
        self.super_mana_potion_spell_info[DB.spell_column_info["EffectBasePoints1"]] = 1999
        self.super_mana_potion_spell_info[DB.spell_column_info["EffectDieSides1"]] = 1
        self.super_mana_potion_spell_info[DB.spell_column_info["EffectBaseDice1"]] = 1
        self.super_mana_potion_spell_info = tuple(self.super_mana_potion_spell_info)

    def test_serpent_coil_braid_spell_mana_emerald(self):
        self.char.combat_handler.apply_spell_effect(self.serpent_coil_braid_spell)
        self.char.combat_handler.energize(self.mana_emerald_spell_info, 1)

        self.assertEqual(2500, self.char.current_mana)

    def test_serpent_coil_braid_spell_super_mana_potion(self):
        self.char.combat_handler.apply_spell_effect(self.serpent_coil_braid_spell)
        self.char.combat_handler.energize(self.super_mana_potion_spell_info, 1)

        self.assertEqual(2000, self.char.current_mana)

    def test_serpent_coil_braid_spell_mana_ruby(self):
        self.char.combat_handler.apply_spell_effect(self.serpent_coil_braid_spell)
        self.char.combat_handler.energize(self.mana_ruby_spell_info, 1)

        self.assertEqual(2500, self.char.current_mana)

    def test_mana_surge_effect_mana_emerald(self):
        self.char.combat_handler.apply_spell_effect(self.serpent_coil_braid_spell)

        self.assertFalse(any(aura.spell_id == 37445 for aura in self.char.combat_handler.active_auras))

        self.char.combat_handler.use_item(self.super_mana_potion)
        self.assertFalse(any(aura.spell_id == 37445 for aura in self.char.combat_handler.active_auras))

        self.char.combat_handler.use_item(self.mana_emerald)
        self.assertTrue(any(aura.spell_id == 37445 for aura in self.char.combat_handler.active_auras))
