from pydantic import BaseModel, ConfigDict

from app.models.pokemon_type import PokemonType


class SpeciesBase(BaseModel):
    name: str
    dex_number: int
    form: str = "Normal"
    base_attack: int
    base_defense: int
    base_stamina: int
    type1: PokemonType
    type2: PokemonType | None = None


class SpeciesCreate(SpeciesBase):
    pass


class SpeciesRead(SpeciesBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
