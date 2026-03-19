from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[List["Character"]] = relationship(back_populates="author")
    favorite_planets: Mapped[List["Planet"]] = relationship(back_populates="author")
    favorite_species: Mapped[List["Species"]] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    users_who_favorite: Mapped[List["User"]] = relationship(back_populates="author")

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    characters: Mapped[List["Character"]] = relationship(back_populates="author")
    description: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    users_who_favorite: Mapped[List["User"]] = relationship(back_populates="author")

class Species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    characters: Mapped[List["Character"]] = relationship(back_populates="author")
    planets: Mapped[List["Planet"]] = relationship(back_populates="author")

class Favorites(db.Model):
    user: Mapped[int] = mapped_column(primary_key=True)
    favorite_characters: Mapped[int] = mapped_column(ForeignKey("user.favorite_characters"))
    favorite_planets: Mapped[int] = mapped_column(ForeignKey("user.favorite_planets"))
    favorite_species: Mapped[int] = mapped_column(ForeignKey("user.favorite_species"))
