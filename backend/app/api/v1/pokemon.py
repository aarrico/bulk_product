import csv
import io
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.models.pokemon import Gender, ShadowStatus
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

@router.post("/import")
async def import_pokemon(file: UploadFile, db: AsyncSession = Depends(get_db)):
    content = await file.read()
    raw_data = csv.DictReader(io.StringIO(content.decode("utf-8")))
    pkmn_data: list[PokemonCreate] = []

    shadow_map = {0: "normal", 1: "shadow", 2: "purified"}
    gender_map = {"♂": "male", "♀": "female"}

    try:
        for pkmn in raw_data:
            shadow_val = int(pkmn["Shadow/Purified"])

            try:
                shadow_status = ShadowStatus(shadow_map[shadow_val])
            except KeyError as e:
                raise ValueError(f"Unexpected Shadow/Purified value: {shadow_val}") from e

            pkmn_data.append(PokemonCreate(
                dex_number=int(pkmn["Pokemon"]),
                attack_iv=int(pkmn["Atk IV"]),
                defense_iv=int(pkmn["Def IV"]),
                stamina_iv=int(pkmn["Sta IV"]),
                level=float(pkmn["Level Min"]),
                gender=Gender(gender_map.get(pkmn["Gender"], "genderless")),
                shadow_status=shadow_status,
                lucky=pkmn["Lucky"] == "1",
            ))
    except (ValueError, KeyError) as e:
        raise HTTPException(400, f"Malformed CSV: {e}") from e

    await pokemon_service.sync_pokemon(db, pkmn_data)

    await db.commit()

    return {"message": "Pokégenie scan successfully synced!"}
