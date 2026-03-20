import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pokemon import Pokemon
from app.models.species import Species
from app.schemas.pokemon import PokemonCreate, PokemonFilter
from app.services import species as species_service


async def create_pokemon(db: AsyncSession, data: PokemonCreate) -> Pokemon:
    species = await species_service.get_species_by_dex_number(db, data.dex_number)

    if not species:
        raise ValueError(f"Species with dex number {data.dex_number} not found")

    pokemon = Pokemon(**data.model_dump(exclude={"dex_number"}), species_id=species.id)

    db.add(pokemon)
    await db.flush()
    await db.refresh(pokemon)

    return pokemon

async def get_pokemon_by_id(db: AsyncSession, id: uuid.UUID) -> Pokemon | None:
    return await db.get(Pokemon, id)

async def get_all_pokemon(db: AsyncSession, filters: PokemonFilter) -> Sequence[Pokemon]:
    query = select(Pokemon)

    if filters.species_id is not None:
        query = query.where(Pokemon.species_id == filters.species_id)
    if filters.species_name is not None:
        query = query.join(Species).where(Species.name == filters.species_name)
    if filters.type1 is not None:
        query = query.join(Species).where(Species.type1 == filters.type1)
    if filters.type2 is not None:
        query = query.join(Species).where(Species.type2 == filters.type2)
    if filters.attack_iv_min is not None:
        query = query.where(Pokemon.attack_iv >= filters.attack_iv_min)
    if filters.attack_iv_max is not None:
        query = query.where(Pokemon.attack_iv <= filters.attack_iv_max)
    if filters.defense_iv_min is not None:
        query = query.where(Pokemon.defense_iv >= filters.defense_iv_min)
    if filters.defense_iv_max is not None:
        query = query.where(Pokemon.defense_iv <= filters.defense_iv_max)
    if filters.stamina_iv_min is not None:
        query = query.where(Pokemon.stamina_iv >= filters.stamina_iv_min)
    if filters.stamina_iv_max is not None:
        query = query.where(Pokemon.stamina_iv <= filters.stamina_iv_max)
    if filters.level_min is not None:
        query = query.where(Pokemon.level >= filters.level_min)
    if filters.level_max is not None:
        query = query.where(Pokemon.level <= filters.level_max)
    if filters.shadow_status is not None:
        query = query.where(Pokemon.shadow_status == filters.shadow_status)
    if filters.lucky is not None:
        query = query.where(Pokemon.lucky == filters.lucky)
    if filters.best_buddy is not None:
        query = query.where(Pokemon.best_buddy == filters.best_buddy)
    if filters.shiny is not None:
        query = query.where(Pokemon.shiny == filters.shiny)
    if filters.gender is not None:
        query = query.where(Pokemon.gender == filters.gender)
    if filters.size is not None:
        query = query.where(Pokemon.size == filters.size)
    if filters.nickname is not None:
        query = query.where(Pokemon.nickname.ilike(f"%{filters.nickname}%"))

    result = await db.execute(query)
    return result.scalars().all()