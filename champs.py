from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List


class Stat(Enum):
    HEALTH = auto()
    HEALTH_REGEN = auto()
    MANA = auto()
    MANA_REGEN = auto()

    AD = auto()
    AP = auto()

    ARMOR = auto()
    MAGIC_RESIST = auto()

    ATTACK_SPEED = auto()
    ABILITY_HASTE = auto()
    CRIT_CHANCE = auto()
    CRIT_DAMAGE = auto()

    MOVE_SPEED = auto()

    LETHALITY = auto()
    ARMOR_PEN_PERCENT = auto()
    MAGIC_PEN_FLAT = auto()
    MAGIC_PEN_PERCENT = auto()

    LIFE_STEAL = auto()
    OMNIVAMP = auto()

    TENACITY = auto()

@dataclass
class StatBlock:
    values: Dict[Stat, float] = field(default_factory=dict)

    def get(self, stat: Stat) -> float:
        return self.values.get(stat, 0.0)

    def add(self, stat: Stat, value: float):
        self.values[stat] = self.get(stat) + value

    def add_block(self, other: "StatBlock"):
        for stat, value in other.values.items():
            self.add(stat, value)

    def multiply(self, stat: Stat, percent: float):
        self.values[stat] = self.get(stat) * percent


@dataclass
class Modifier:
    name: str
    stats: StatBlock

@dataclass
class Item:
    name: str
    cost: int
    stats: StatBlock
    modifiers: List[Modifier] = field(default_factory=list)

    def get_total_stats(self) -> StatBlock:
        total = StatBlock()
        total.add_block(self.stats)

        for mod in self.modifiers:
            total.add_block(mod.stats)

        return total

@dataclass
class Rune:
    name: str
    stats: StatBlock

@dataclass
class RunePage:
    runes: List[Rune]

    def get_total_stats(self) -> StatBlock:
        total = StatBlock()

        for rune in self.runes:
            total.add_block(rune.stats)

        return total
    


@dataclass
class ChampionStats:
    base: StatBlock
    growth: StatBlock

    def at_level(self, level: int) -> StatBlock:
        stats = StatBlock()

        for stat in Stat:
            base_val = self.base.get(stat)
            growth_val = self.growth.get(stat)

            value = base_val + growth_val * (level - 1)
            if value > 0:
                stats.add(stat, value)

        return stats
    

@dataclass
class Champion:
    name: str
    level: int
    base_stats: ChampionStats

    items: List[Item] = field(default_factory=list)
    rune_page: RunePage = field(default_factory=lambda: RunePage([]))
    modifiers: List[Modifier] = field(default_factory=list)

    def get_total_stats(self) -> StatBlock:

        total = StatBlock()

        # base stats
        total.add_block(self.base_stats.at_level(self.level))

        # items
        for item in self.items:
            total.add_block(item.get_total_stats())

        # runes
        total.add_block(self.rune_page.get_total_stats())

        # modifiers (buffs)
        for mod in self.modifiers:
            total.add_block(mod.stats)

        return total

    def get_stat(self, stat: Stat) -> float:
        return self.get_total_stats().get(stat)