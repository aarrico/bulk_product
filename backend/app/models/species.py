from __future__ import annotations

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base
from app.models.pokemon_type import PokemonType


class Species(Base):
    __tablename__ = "species"
    __table_args__ = (UniqueConstraint("dex_number", "form"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dex_number: Mapped[int] = mapped_column(index=True)
    form: Mapped[str] = mapped_column(String(30), default="Normal")
    base_attack: Mapped[int]
    base_defense: Mapped[int]
    base_stamina: Mapped[int]
    type1: Mapped[PokemonType] = mapped_column(Enum(PokemonType))
    type2: Mapped[PokemonType | None] = mapped_column(Enum(PokemonType))
