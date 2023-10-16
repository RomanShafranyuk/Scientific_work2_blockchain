import datetime
from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.functions import sum as sum_string
from sqlalchemy.sql.expression import desc
import random

engine = create_engine('sqlite:///test.db?check_same_thread=False')


def create_session():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


# db_session =scoped_session(sessionmaker(autocommit=False,
#                                        autoflush=False,
#                                        bind=engine))
Base = declarative_base()



def init_db(db_session):
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)


def add_block(db_session, name1: str, amount: int, name2: str, hash_: str, prev_index):
    
    b = Block(name1, amount, name2, hash_, prev_index)
    check_list = []
    while len(check_list) == 0:
        db_session.add(b)
        flag = db_session.commit()
        print(flag)
        check_list += db_session.query(Block.number_id).select_from(Block).where(
            Block.amount == amount).where(Block.who == name1).where(Block.to_whom == name2).where(Block.block_hash == hash_).all()


def get_last_block(db_session):
    return db_session.query(Block.who, Block.amount, Block.to_whom, Block.block_hash, Block.number_id).select_from(Block).order_by(desc(Block.number_id)).limit(1).all()[0]


def is_database_empty(db_session):
    return db_session.query(count(Block.number_id)).all()[0][0] == 0

def get_block_id(db_session, name):
    return db_session.query(Block.number_id).where(Block.who == name).all()[0][0]


def get_average_time():
    db_session = create_session()
    sum = db_session.query(sum_string(Timer.time)).all()[0][0]
    count_blocks = db_session.query(count(Timer.time)).all()[0][0]
    return sum / count_blocks


def add_time(db_session, name, time):
    n_id = get_block_id(db_session, name)
    t = Timer(n_id, time)
    db_session.add(t)
    db_session.commit()


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

class Timer(Base):
    __tablename__ = 'timer'
    n_id = Column(Integer, ForeignKey('blocks.number_id'), primary_key=True)
    number = relationship('Block')
    time = Column(Float)

    def __init__(self, number_id, time):
        self.n_id = number_id
        self.time = time



session = create_session()
init_db(session)

