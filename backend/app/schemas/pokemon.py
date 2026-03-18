import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pokemon import BestBuddyStatus, Gender, ShadowStatus, Size


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


class PokemonRead(PokemonBase):
    id: uuid.UUID
    species_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
