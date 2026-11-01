from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.producto_model import Producto

class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)

    productos: Mapped[list["Producto"]] = relationship(back_populates="categoria")