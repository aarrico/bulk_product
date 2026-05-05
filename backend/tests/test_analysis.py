import pytest

from app.core.analysis import (
    AnalysisResult,
    analyze,
    analyze_ranked,
    find_rank_one,
)
from app.core.leagues import LEAGUES, League
from app.core.stats import LEVELS, BaseStats, IVs

WEAK_BASE = BaseStats(attack=80, defense=80, stamina=120)
BALANCED_BASE = BaseStats(attack=200, defense=200, stamina=200)
STRONG_BASE = BaseStats(attack=290, defense=170, stamina=240)
EXTREME_BASE = BaseStats(attack=1000, defense=1000, stamina=1000)

PERFECT_IVS = IVs(15, 15, 15)
LOW_ATK_IVS = IVs(0, 15, 15)
ZERO_IVS = IVs(0, 0, 0)

GREAT = LEAGUES["great"]
ULTRA = LEAGUES["ultra"]
MASTER = LEAGUES["master"]
LITTLE = LEAGUES["little"]


def test_analyze_master_league_uses_max_level() -> None:
    result = analyze(BALANCED_BASE, PERFECT_IVS, MASTER)
    assert result is not None
    assert result.level == LEVELS[-1]


def test_analyze_returns_none_when_l1_exceeds_cap() -> None:
    assert analyze(EXTREME_BASE, PERFECT_IVS, LITTLE) is None


def test_analyze_capped_league_respects_cap() -> None:
    result = analyze(BALANCED_BASE, LOW_ATK_IVS, GREAT)
    assert result is not None
    assert result.cp <= GREAT.cp_cap  # type: ignore[operator]
    assert result.ivs == LOW_ATK_IVS


def test_analyze_stat_product_positive() -> None:
    result = analyze(WEAK_BASE, PERFECT_IVS, GREAT)
    assert result is not None
    assert result.stat_product > 0


@pytest.mark.parametrize("league", [LITTLE, GREAT, ULTRA])
def test_find_rank_one_under_cap(league: League) -> None:
    rank_one = find_rank_one(BALANCED_BASE, league)
    assert rank_one.cp <= league.cp_cap  # type: ignore[operator]


def test_find_rank_one_master_is_perfect_ivs() -> None:
    rank_one = find_rank_one(BALANCED_BASE, MASTER)
    assert rank_one.ivs == PERFECT_IVS
    assert rank_one.level == LEVELS[-1]


@pytest.mark.parametrize(
    "base,league",
    [
        (WEAK_BASE, GREAT),
        (BALANCED_BASE, GREAT),
        (BALANCED_BASE, ULTRA),
        (STRONG_BASE, GREAT),
    ],
)
def test_find_rank_one_is_actually_optimal(base: BaseStats, league: League) -> None:
    rank_one = find_rank_one(base, league)
    for atk in range(16):
        for dfn in range(16):
            for sta in range(16):
                candidate = analyze(base, IVs(atk, dfn, sta), league)
                if candidate is None:
                    continue
                assert candidate.stat_product <= rank_one.stat_product


def test_find_rank_one_is_cached() -> None:
    first = find_rank_one(BALANCED_BASE, GREAT)
    second = find_rank_one(BALANCED_BASE, GREAT)
    assert first is second


def test_analyze_ranked_perfect_at_rank_one_ivs() -> None:
    rank_one = find_rank_one(BALANCED_BASE, GREAT)
    ranked = analyze_ranked(BALANCED_BASE, rank_one.ivs, GREAT)
    assert ranked is not None
    assert ranked.rank_percentage == pytest.approx(100.0)


@pytest.mark.parametrize(
    "ivs",
    [PERFECT_IVS, LOW_ATK_IVS, ZERO_IVS, IVs(7, 8, 9), IVs(15, 0, 15)],
)
def test_analyze_ranked_never_exceeds_one_hundred(ivs: IVs) -> None:
    ranked = analyze_ranked(BALANCED_BASE, ivs, GREAT)
    assert ranked is not None
    assert ranked.rank_percentage <= 100.0 + 1e-9


def test_analyze_ranked_returns_none_when_analyze_returns_none() -> None:
    assert analyze_ranked(EXTREME_BASE, PERFECT_IVS, LITTLE) is None


def test_analysis_result_is_immutable() -> None:
    result = analyze(BALANCED_BASE, PERFECT_IVS, GREAT)
    assert result is not None
    with pytest.raises(AttributeError):
        result.cp = 9999  # type: ignore[misc]


def test_analyze_result_type() -> None:
    result = analyze(BALANCED_BASE, PERFECT_IVS, GREAT)
    assert isinstance(result, AnalysisResult)
