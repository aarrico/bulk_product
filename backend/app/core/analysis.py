from dataclasses import dataclass
from functools import lru_cache

from app.core.leagues import League
from app.core.stats import (
    LEVELS,
    BaseStats,
    IVs,
    calculate_cp,
    calculate_stat_product,
    find_optimal_level,
)


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    ivs: IVs
    level: float
    cp: int
    stat_product: float


@dataclass(frozen=True, slots=True)
class RankedAnalysisResult:
    analysis: AnalysisResult
    rank_one: AnalysisResult
    rank_percentage: float


def _optimal_level(base: BaseStats, ivs: IVs, cp_cap: int | None) -> float | None:
    if cp_cap is None:
        return LEVELS[-1]
    return find_optimal_level(base, ivs, cp_cap)


def analyze(base: BaseStats, ivs: IVs, league: League) -> AnalysisResult | None:
    level = _optimal_level(base, ivs, league.cp_cap)
    if level is None:
        return None
    return AnalysisResult(
        ivs=ivs,
        level=level,
        cp=calculate_cp(base, ivs, level),
        stat_product=calculate_stat_product(base, ivs, level),
    )


@lru_cache(maxsize=None)
def find_rank_one(base: BaseStats, league: League) -> AnalysisResult:
    best: AnalysisResult | None = None
    for atk in range(16):
        for dfn in range(16):
            for sta in range(16):
                result = analyze(base, IVs(atk, dfn, sta), league)
                if result is None:
                    continue
                if best is None or result.stat_product > best.stat_product:
                    best = result
    if best is None:
        raise ValueError(f"No valid IV spread for base={base} in league={league.name}")
    return best


def analyze_ranked(
    base: BaseStats, ivs: IVs, league: League
) -> RankedAnalysisResult | None:
    analysis = analyze(base, ivs, league)
    if analysis is None:
        return None
    rank_one = find_rank_one(base, league)
    return RankedAnalysisResult(
        analysis=analysis,
        rank_one=rank_one,
        rank_percentage=analysis.stat_product / rank_one.stat_product * 100,
    )
