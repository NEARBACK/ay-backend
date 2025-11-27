from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_amount_nanoton: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    author: Mapped["Users"] = relationship("Users", back_populates="posts")  # type: ignore # noqa F821
    donations: Mapped[list["Donations"]] = relationship(  # type: ignore # noqa F821
        "Donations", back_populates="post", cascade="all, delete-orphan"
    )
    media: Mapped[list["Media"]] = relationship(  # type: ignore # noqa F821
        "Media", back_populates="post", cascade="all, delete-orphan"
    )
