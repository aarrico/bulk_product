from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
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
    stmt = select(Species).where(Species.dex_number == dex_num)
    data = await db.execute(stmt)
    return data.scalar_one_or_none()


async def get_species_by_name(db: AsyncSession, name: str) -> Species | None:
    stmt = select(Species).where(Species.name == name)
    data = await db.execute(stmt)
    return data.scalar_one_or_none()


async def get_all_species(db: AsyncSession) -> Sequence[Species]:
    stmt = select(Species)
    data = await db.execute(stmt)
    return data.scalars().all()


async def bulk_update_species(db: AsyncSession, species: list[SpeciesCreate]) -> None:
    stmt = insert(Species).values([s.model_dump() for s in species])
    stmt = stmt.on_conflict_do_update(
        index_elements=["dex_number", "form"],
        set_={
            "name": stmt.excluded.name,
            "base_attack": stmt.excluded.base_attack,
            "base_defense": stmt.excluded.base_defense,
            "base_stamina": stmt.excluded.base_stamina,
            "type1": stmt.excluded.type1,
            "type2": stmt.excluded.type2,
        },
    )

    await db.execute(stmt)
