from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_cheese_types(db: Session) -> list[models.DBCheeseType]:
    return db.scalars(select(models.DBCheeseType)).all()


def get_cheese_type_by_id(
    db: Session, cheese_type_id: int
) -> models.DBCheeseType | None:
    return db.scalar(
        select(models.DBCheeseType).where(models.DBCheeseType.id == cheese_type_id)
    )


def create_cheese_type(
    db: Session,
    cheese_type: schemas.CheeseTypeCreate
) -> models.DBCheeseType:
    db_cheese_type = models.DBCheeseType(
        name=cheese_type.name,
        description=cheese_type.description,
    )
    db.add(db_cheese_type)
    db.commit()
    db.refresh(db_cheese_type)

    return db_cheese_type


def get_cheese_type_by_name(db: Session, name: str) -> models.DBCheeseType | None:
    return db.scalar(
        select(models.DBCheeseType).where(models.DBCheeseType.name == name)
    )


def get_cheese_list(
    db: Session,
    packaging_type: models.PackagingType | None = None,
    cheese_type: str | None = None,
) -> list[models.DBCheese]:
    stmt = select(models.DBCheese)

    if packaging_type:
        stmt = stmt.where(models.DBCheese.packaging_type == packaging_type)

    if cheese_type:
        stmt = stmt.join(models.DBCheeseType).where(models.DBCheeseType.name == cheese_type)

    return db.scalars(stmt).all()


def get_cheese_by_id(db: Session, cheese_id: int) -> models.DBCheese | None:
    return db.scalar(select(models.DBCheese).where(models.DBCheese.id == cheese_id))


def get_cheese_by_title(db: Session, title: str) -> models.DBCheese | None:
    return db.scalar(select(models.DBCheese).where(models.DBCheese.title == title))


def create_cheese(db: Session, cheese: schemas.CheeseCreate) -> models.DBCheese:
    db_cheese = models.DBCheese(
        cheese_type_id=cheese.cheese_type_id,
        title=cheese.title,
        price=cheese.price,
        packaging_type=cheese.packaging_type,
    )
    db.add(db_cheese)
    db.commit()
    db.refresh(db_cheese)

    return db_cheese
