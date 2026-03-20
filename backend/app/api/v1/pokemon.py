import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.schemas.pokemon import PokemonCreate, PokemonFilter, PokemonRead
from app.services import pokemon as pokemon_service

router = APIRouter()

@router.post("/", response_model=PokemonRead)
async def create_pokemon(data: PokemonCreate, db: AsyncSession = Depends(get_db)):
    try:
        pokemon = await pokemon_service.create_pokemon(db, data)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e

    await db.commit()
    return pokemon

@router.get("/{id}", response_model=PokemonRead)
async def get_pokemon_by_id(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    pokemon = await pokemon_service.get_pokemon_by_id(db, id)
    if not pokemon:
        raise HTTPException(404, "Pokemon not found")
    return pokemon

@router.get("/", response_model=list[PokemonRead])
async def get_all_pokemon(filters: PokemonFilter = Depends(), db: AsyncSession = Depends(get_db)):
    return await pokemon_service.get_all_pokemon(db, filters)
