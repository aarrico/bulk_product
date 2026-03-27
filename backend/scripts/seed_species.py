import asyncio
import re
from typing import Any

import httpx

from app.core.database import async_session
from app.schemas.species import SpeciesCreate
from app.services.species import bulk_update_species

SPECIES_NAME_PATTERN = r"\((.+)\)"


def map_to_species(entry: dict) -> SpeciesCreate:
    name = entry["speciesName"]
    type2 = entry["types"][1].lower() if entry["types"][1] != "none" else None

    match = re.search(SPECIES_NAME_PATTERN, name)
    form = match.group(1) if match else "Normal"
    clean_name = re.sub(SPECIES_NAME_PATTERN, "", name).strip()

    return SpeciesCreate(
        name=clean_name,
        dex_number=entry["dex"],
        base_attack=entry["baseStats"]["atk"],
        base_defense=entry["baseStats"]["def"],
        base_stamina=entry["baseStats"]["hp"],
        type1=entry["types"][0].lower(),
        type2=type2,
        form=form,
    )


def build_species_list(data: Any) -> list[SpeciesCreate]:
    seen: set[tuple[int, str]] = set()
    species_data: list[SpeciesCreate] = []
    for entry in data:
        sid = entry["speciesId"]
        if any(x in sid for x in ("_shadow", "_mega", "_primal")):
            continue
        species = map_to_species(entry)
        key = (species.dex_number, species.form)
        if key in seen:
            continue
        seen.add(key)
        species_data.append(species)

    return species_data


async def seed_species():
    resp = httpx.get(
        "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster/pokemon.json"
    )
    data = resp.json()

    species_data = build_species_list(data)

    async with async_session() as db:
        await bulk_update_species(db, species_data)
        await db.commit()


asyncio.run(seed_species())
