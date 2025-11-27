from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Media(Base):
    __tablename__ = "media"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    url = mapped_column(String(700), nullable=False)
    post_id = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    post: Mapped["Posts"] = relationship("Posts", back_populates="media")  # type: ignore # noqa F821
