import os
import sys
from sqlalchemy import Column,ForeignKey, Integer, String, Enum,DateTime,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class MyEnum(Enum):
    Male = 1
    Female = 2


Base = declarative_base()

class Shelter(Base):

    __tablename__   = 'shelter'

    id              = Column(Integer, primary_key = True)
    name            = Column(String(20), nullable = False)
    address         = Column(String(100),nullable = False)
    city            = Column(String(15))
    state           = Column(String(15))
    zipCode         = Column(String(15))
    website         = Column(String(20))


class Puppy(Base):

    __tablename__   = 'puppy'
    id              = Column(Integer,primary_key = True)
    name            = Column(String(20), nullable = False)
    date_of_birth   = Column(Date)
    gender          = Column(Enum('male','female'))
    weight          = Column(Integer, nullable = True, default = 10)
    shelter_id      = Column(Integer, ForeignKey('shelter.id'))
    picture         = Column(String)
    shelter         = relationship(Shelter)
engine = create_engine('sqlite:///shelter.db')

Base.metadata.create_all(engine)
