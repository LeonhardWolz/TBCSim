from dataclasses import dataclass, field
from typing import List


@dataclass
class Aura:
    spell_id: int
    aura_id: int
    value: int
    misc_value: int
    affected_spell_school: int
    affected_spell_family_mask: int = 0
    affected_item_class: int = 0
    affected_item_subclass_mask: int = 0
    create_time: int = 0
    duration_index: int = 0
    trigger_spell: int = 0
    curr_stacks: int = 1
    stack_limit: int = 1
    proc_counter: int = 0
    proc: List = field(default_factory=lambda: [0, 0, 0, 0])
    attributes: List = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0])

    def procced(self):
        self.proc_counter += 1
