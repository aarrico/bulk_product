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


class Pokemon(Base):
    __tablename__ = "pokemon"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid7)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), index=True)
    species: Mapped[Species] = relationship()
    attack_iv: Mapped[int]
    defense_iv: Mapped[int]
    stamina_iv: Mapped[int]
    level: Mapped[float] = mapped_column(Numeric(precision=3, scale=1))
    shadow_status: Mapped[ShadowStatus] = mapped_column(default=ShadowStatus.NORMAL)
    nickname: Mapped[str | None] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
