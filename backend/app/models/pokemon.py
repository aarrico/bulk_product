import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base
from app.models.species import Species


class ShadowStatus(StrEnum):
    NORMAL = "normal"
    SHADOW = "shadow"
    PURIFIED = "purified"


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    GENDERLESS = "genderless"


class Size(StrEnum):
    XXS = "xxs"
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"
    XXL = "xxl"


class BestBuddyStatus(StrEnum):
    NONE = "none"
    ACHIEVED = "achieved"
    ACTIVE = "active"

class Pokemon(Base):
    __tablename__ = "pokemon"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid7)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), index=True)
    species: Mapped[Species] = relationship(lazy="joined")
    attack_iv: Mapped[int]
    defense_iv: Mapped[int]
    stamina_iv: Mapped[int]
    level: Mapped[float] = mapped_column(Numeric(precision=3, scale=1))
    shadow_status: Mapped[ShadowStatus] = mapped_column(default=ShadowStatus.NORMAL)
    lucky: Mapped[bool] = mapped_column(default=False)
    best_buddy: Mapped[BestBuddyStatus] = mapped_column(default=BestBuddyStatus.NONE)
    shiny: Mapped[bool] = mapped_column(default=False)
    gender: Mapped[Gender]
    size: Mapped[Size | None] = mapped_column(default=None)
    nickname: Mapped[str | None] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
