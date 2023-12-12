from typing import List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Home(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    members: List["Member"] = Relationship(back_populates="home")


class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    home_id: Optional[int] = Field(default=None, foreign_key="home.id")
    home: Optional[Home] = Relationship(back_populates="members")