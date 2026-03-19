from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.species import Species
from app.schemas.species import SpeciesCreate


async def create_species(db: AsyncSession, data: SpeciesCreate) -> Species:
    species = Species(**data.model_dump())
    db.add(species)
    await db.flush()
    await db.refresh(species)

    return species

async def get_species_by_id(db: AsyncSession, id: int) -> Species | None:
    return await db.get(Species, id)

async def get_species_by_dex_number(db: AsyncSession, dex_num: int) -> Species | None:
    query = select(Species).where(Species.dex_number == dex_num)
    data = await db.execute(query)
    return data.scalar_one_or_none()

async def get_species_by_name(db: AsyncSession, name: str) -> Species | None:
    query = select(Species).where(Species.name == name)
    data = await db.execute(query)
    return data.scalar_one_or_none()

async def get_all_species(db: AsyncSession) -> Sequence[Species]:
    query = select(Species)
    data = await db.execute(query)
    return data.scalars().all()
