from sqlalchemy.orm import DeclarativeBase

from random_generator.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
