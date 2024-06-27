from datetime import datetime

from sqlalchemy import create_engine, FetchedValue
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import Column, Integer, String, ForeignKey, REAL, Boolean, DateTime
from sqlalchemy.orm import relationship

DatabaseUrl = "mysql://isp_p_Kacion:12345@77.91.86.135/isp_p_Kacion"
engine = create_engine(DatabaseUrl)

class Base(DeclarativeBase):
    pass

class WorkWear(Base):
    __tablename__ = "WorkWear"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    wear_type = Column(String(50), nullable=False)
    period_of_wearing = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)

class Workshop(Base):
    __tablename__ = "Workshop"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    workshop_name = Column(String(50), nullable=False)
    chief_name = Column(String(50), nullable=False)

class Workers(Base):
    __tablename__ = "Workers"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    name = Column(String(50), nullable=False)
    post = Column(String(50), nullable=False)
    discount_on_clothes = Column(Integer, nullable=False)

class GetGoods(Base):
    __tablename__ = "GetGoods"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    worker_id = Column(Integer, nullable=False)
    clothes_id = Column(Integer, nullable=False)
    goods_date_get = Column(DateTime, nullable=False)
    painting = Column(String(50), nullable=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)