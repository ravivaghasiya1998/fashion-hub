from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, Text

from fashion_hub_backend.database.db_setup import Base
from fashion_hub_backend.schemas.categories.schemas import CategoryName


class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[CategoryName] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
