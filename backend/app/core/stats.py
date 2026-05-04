import json
import math
from dataclasses import dataclass
from pathlib import Path

_CPM_PATH = Path(__file__).parent.parent / "data" / "cpm.json"


def _load_cpm() -> dict[float, float]:
    with _CPM_PATH.open() as f:
        raw = json.load(f)
    return {float(level): cpm for level, cpm in raw.items()}


CPM: dict[float, float] = _load_cpm()
LEVELS: tuple[float, ...] = tuple(sorted(CPM.keys()))


@dataclass(frozen=True, slots=True)
class BaseStats:
    attack: int
    defense: int
    stamina: int


@dataclass(frozen=True, slots=True)
class IVs:
    attack: int
    defense: int
    stamina: int


def effective_stat(base: int, iv: int, cpm: float) -> float:
    return (base + iv) * cpm


def calculate_cp(base: BaseStats, ivs: IVs, level: float) -> int:
    cpm = CPM[level]
    eff_atk = effective_stat(base.attack, ivs.attack, cpm)
    eff_def = effective_stat(base.defense, ivs.defense, cpm)
    eff_sta = effective_stat(base.stamina, ivs.stamina, cpm)
    return max(10, math.floor((eff_atk * math.sqrt(eff_def) * math.sqrt(eff_sta)) / 10))


def calculate_stat_product(base: BaseStats, ivs: IVs, level: float) -> float:
    cpm = CPM[level]
    eff_atk = effective_stat(base.attack, ivs.attack, cpm)
    eff_def = effective_stat(base.defense, ivs.defense, cpm)
    eff_sta = effective_stat(base.stamina, ivs.stamina, cpm)
    return eff_atk * eff_def * math.floor(eff_sta)


def find_optimal_level(base: BaseStats, ivs: IVs, cp_cap: int) -> float | None:
    for level in reversed(LEVELS):
        if calculate_cp(base, ivs, level) <= cp_cap:
            return level
    return None
