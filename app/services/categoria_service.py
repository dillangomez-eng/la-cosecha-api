from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria
from app.schemas.categoria_schema import CategoriaCrear


def listar_categorias(db: Session) -> list[Categoria]:
    return list(db.scalars(select(Categoria).order_by(Categoria.id)))


def buscar_categoria(db: Session, categoria_id: int) -> Categoria | None:
    return db.get(Categoria, categoria_id)


def buscar_por_nombre(db: Session, nombre: str):
    return db.scalar(select(Categoria).where(Categoria.nombre == nombre))


def crear_categoria(db: Session, datos: CategoriaCrear) -> Categoria:
    categoria = Categoria(nombre=datos.nombre)
    db.add(categoria)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(categoria)
    return categoria


def actualizar_categoria(
    db: Session, categoria_id: int, datos: CategoriaCrear
) -> Categoria | None:
    categoria = buscar_categoria(db, categoria_id)
    if categoria is None:
        return None
    categoria.nombre = datos.nombre
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(categoria)
    return categoria


def eliminar_categoria(db: Session, categoria_id: int) -> bool:
    categoria = buscar_categoria(db, categoria_id)
    if categoria is None:
        return False
    db.delete(categoria)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    return True
