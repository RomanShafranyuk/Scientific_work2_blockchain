import datetime
from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import desc
import random

engine = create_engine('sqlite:///test.db?check_same_thread=False')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def add_block(name1: str, amount: int, name2: str, hash_: str, prev_index):
    b = Block(name1, amount, name2, hash_, prev_index)
    check_list = []
    while len(check_list) == 0:
        db_session.add(b)
        db_session.commit()
        check_list += db_session.query(Block.number_id).select_from(Block).where(
            Block.amount == amount).where(Block.who == name1).where(Block.to_whom == name2).where(Block.block_hash == hash_).all()

def get_block_data():
    return db_session.query(Block.who, Block.amount, Block.to_whom, Block.block_hash, Block.number_id).select_from(Block).order_by(desc(Block.number_id)).limit(1).all()[0]


    

def is_database_exist():
    return db_session.query(count(Block.number_id)).all()[0][0] == 0

class Block(Base):
    __tablename__ = 'blocks'
    number_id = Column(Integer, primary_key=True)
    who = Column(String(100), nullable=True)
    amount = Column(Integer)
    to_whom = Column(String(100), nullable=True)
    block_hash = Column(String(100), nullable=True)
    prev_index = Column(Integer)

    def __init__(self, name1, amount, name2, hash_, prev_index):
        self.who = name1
        self.amount = amount
        self.to_whom = name2
        self.block_hash = hash_
        self.prev_index = prev_index




