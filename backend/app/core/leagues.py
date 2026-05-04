from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class League:
    name: str
    cp_cap: int | None


LEAGUES: dict[str, League] = {
    "little": League("Little", 500),
    "great": League("Great", 1500),
    "ultra": League("Ultra", 2500),
    "master": League("Master", None),
}
