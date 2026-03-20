import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pokemon import BestBuddyStatus, Gender, ShadowStatus, Size
from app.models.pokemon_type import PokemonType


class PokemonBase(BaseModel):
    attack_iv: int = Field(ge=0, le=15)
    defense_iv: int = Field(ge=0, le=15)
    stamina_iv: int = Field(ge=0, le=15)
    level: float = Field(ge=1, le=51)
    shadow_status: ShadowStatus = ShadowStatus.NORMAL
    lucky: bool = False
    best_buddy: BestBuddyStatus = BestBuddyStatus.NONE
    shiny: bool = False
    gender: Gender
    size: Size | None = None
    nickname: str | None = None


class PokemonCreate(PokemonBase):
    dex_number: int


class PokemonFilter(BaseModel):
    species_id: int | None = None
    species_name: str | None = None
    type1: PokemonType | None = None
    type2: PokemonType | None = None
    attack_iv_min: int | None = Field(default=None, ge=0, le=15)
    attack_iv_max: int | None = Field(default=None, ge=0, le=15)
    defense_iv_min: int | None = Field(default=None, ge=0, le=15)
    defense_iv_max: int | None = Field(default=None, ge=0, le=15)
    stamina_iv_min: int | None = Field(default=None, ge=0, le=15)
    stamina_iv_max: int | None = Field(default=None, ge=0, le=15)
    level_min: float | None = Field(default=None, ge=1, le=51)
    level_max: float | None = Field(default=None, ge=1, le=51)
    shadow_status: ShadowStatus | None = None
    lucky: bool | None = None
    best_buddy: BestBuddyStatus | None = None
    shiny: bool | None = None
    gender: Gender | None = None
    size: Size | None = None
    nickname: str | None = None


class PokemonRead(PokemonBase):
    id: uuid.UUID
    species_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
