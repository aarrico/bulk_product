from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.schemas.species import SpeciesCreate, SpeciesRead
from app.services import species as species_service

router = APIRouter()


@router.post("/", response_model=SpeciesRead)
async def create_species(data: SpeciesCreate, db: AsyncSession = Depends(get_db)):
    species = await species_service.create_species(db, data)
    await db.commit()
    return species


@router.get("/name/{name}", response_model=SpeciesRead)
async def get_species_by_name(name: str, db: AsyncSession = Depends(get_db)):
    species = await species_service.get_species_by_name(db, name)
    if not species:
        raise HTTPException(404, "Species not found")
    return species


@router.get("/dex/{dex_num}", response_model=SpeciesRead)
async def get_species_by_dex_number(dex_num: int, db: AsyncSession = Depends(get_db)):
    species = await species_service.get_species_by_dex_number(db, dex_num)
    if not species:
        raise HTTPException(404, "Species not found")
    return species


@router.get(path="/{id}", response_model=SpeciesRead)
async def get_species_by_id(id: int, db: AsyncSession = Depends(get_db)):
    species = await species_service.get_species_by_id(db, id)
    if not species:
        raise HTTPException(404, "Species not found")
    return species


@router.get("/", response_model=list[SpeciesRead])
async def get_all_species(db: AsyncSession = Depends(get_db)):
    return await species_service.get_all_species(db)
