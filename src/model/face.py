from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from src.model.base import Base


class Face(Base):
    __tablename__ = "faces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    vector_image: Mapped[List[float]]
