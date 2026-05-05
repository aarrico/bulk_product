import math

import pytest

from app.core.stats import (
    CPM,
    LEVELS,
    SORTED_CPMS,
    BaseStats,
    IVs,
    calculate_cp,
    calculate_stat_product,
    effective_stat,
    find_optimal_level,
)

WEAK_BASE = BaseStats(attack=80, defense=80, stamina=120)
BALANCED_BASE = BaseStats(attack=200, defense=200, stamina=200)
STRONG_BASE = BaseStats(attack=290, defense=170, stamina=240)
EXTREME_BASE = BaseStats(attack=1000, defense=1000, stamina=1000)

PERFECT_IVS = IVs(15, 15, 15)
LOW_ATK_IVS = IVs(0, 15, 15)
ZERO_IVS = IVs(0, 0, 0)


def test_levels_and_cpms_aligned() -> None:
    assert len(LEVELS) == len(SORTED_CPMS)
    assert tuple(CPM[lvl] for lvl in LEVELS) == SORTED_CPMS
    assert list(SORTED_CPMS) == sorted(SORTED_CPMS)


def test_effective_stat_basic() -> None:
    assert effective_stat(100, 15, 0.5) == pytest.approx(57.5)


def test_calculate_cp_minimum_floor() -> None:
    weakling = BaseStats(1, 1, 1)
    assert calculate_cp(weakling, ZERO_IVS, LEVELS[0]) == 10


def test_calculate_cp_monotonic_in_level() -> None:
    cps = [calculate_cp(BALANCED_BASE, PERFECT_IVS, lvl) for lvl in LEVELS]
    assert cps == sorted(cps)


def test_calculate_cp_monotonic_in_ivs() -> None:
    level = 40.0
    assert calculate_cp(BALANCED_BASE, ZERO_IVS, level) < calculate_cp(
        BALANCED_BASE, PERFECT_IVS, level
    )


def test_calculate_cp_matches_canonical_formula() -> None:
    base = BaseStats(100, 100, 100)
    ivs = PERFECT_IVS
    level = 40.0
    cpm = CPM[level]
    expected = math.floor(
        (base.attack + ivs.attack)
        * math.sqrt(base.defense + ivs.defense)
        * math.sqrt(base.stamina + ivs.stamina)
        * cpm**2
        / 10
    )
    assert calculate_cp(base, ivs, level) == expected


def test_stat_product_monotonic_in_level() -> None:
    sps = [calculate_stat_product(BALANCED_BASE, PERFECT_IVS, lvl) for lvl in LEVELS]
    assert sps == sorted(sps)


def test_stat_product_perfect_beats_zero() -> None:
    level = 40.0
    assert calculate_stat_product(
        BALANCED_BASE, PERFECT_IVS, level
    ) > calculate_stat_product(BALANCED_BASE, ZERO_IVS, level)


@pytest.mark.parametrize(
    "base,ivs,cap",
    [
        (WEAK_BASE, PERFECT_IVS, 1500),
        (WEAK_BASE, LOW_ATK_IVS, 500),
        (BALANCED_BASE, PERFECT_IVS, 1500),
        (BALANCED_BASE, LOW_ATK_IVS, 1500),
        (BALANCED_BASE, ZERO_IVS, 2500),
        (STRONG_BASE, PERFECT_IVS, 1500),
        (STRONG_BASE, ZERO_IVS, 500),
        (STRONG_BASE, LOW_ATK_IVS, 2500),
    ],
)
def test_find_optimal_level_is_highest_under_cap(
    base: BaseStats, ivs: IVs, cap: int
) -> None:
    level = find_optimal_level(base, ivs, cap)
    assert level is not None
    assert calculate_cp(base, ivs, level) <= cap

    next_idx = LEVELS.index(level) + 1
    if next_idx < len(LEVELS):
        assert calculate_cp(base, ivs, LEVELS[next_idx]) > cap


def test_find_optimal_level_returns_none_when_l1_exceeds_cap() -> None:
    assert find_optimal_level(EXTREME_BASE, PERFECT_IVS, 500) is None


def test_find_optimal_level_unbound_cap_returns_max_level() -> None:
    assert find_optimal_level(WEAK_BASE, PERFECT_IVS, 100_000) == LEVELS[-1]


def test_find_optimal_level_matches_brute_force() -> None:
    """Closed-form result must equal what a naive linear scan would return."""

    def brute_force(base: BaseStats, ivs: IVs, cap: int) -> float | None:
        for lvl in reversed(LEVELS):
            if calculate_cp(base, ivs, lvl) <= cap:
                return lvl
        return None

    cases = [
        (WEAK_BASE, PERFECT_IVS, 500),
        (WEAK_BASE, ZERO_IVS, 1500),
        (BALANCED_BASE, PERFECT_IVS, 1500),
        (BALANCED_BASE, LOW_ATK_IVS, 1500),
        (BALANCED_BASE, ZERO_IVS, 2500),
        (STRONG_BASE, PERFECT_IVS, 1500),
        (STRONG_BASE, LOW_ATK_IVS, 2500),
        (EXTREME_BASE, PERFECT_IVS, 500),
    ]
    for base, ivs, cap in cases:
        assert find_optimal_level(base, ivs, cap) == brute_force(base, ivs, cap)
