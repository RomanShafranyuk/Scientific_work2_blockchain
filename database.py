from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.functions import sum as sum_string
from sqlalchemy.sql.expression import desc

engine = create_engine(
    'postgresql+psycopg2://postgres:Roman100102_sh@25.22.250.163:5432/blockchain')


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


def get_hashes_list(session) -> list:
    all_hashes_response = session.query(Block.block_hash).all()
    # print(all_hashes_response)
    for i in range(len(all_hashes_response)):
        all_hashes_response[i] = all_hashes_response[i][0]
    return all_hashes_response


def add_block(db_session, new_block):

    b = Block(new_block['name'], new_block['amount'],
              new_block['to whom'], new_block['block_hash'],
              new_block['Merklies_root'], new_block['timestrap'],
              new_block['prev_index'])
    
    check_list = []

    while len(check_list) == 0:
        db_session.add(b)
        db_session.commit()
        check_list += db_session.query(Block.number_id).select_from(Block).where(
            Block.amount == new_block['amount']).where(Block.who == new_block['name']
                                                       ).where(Block.to_whom == new_block['to whom']
                                                               ).where(Block.block_hash == new_block['block_hash']).all()


def get_last_block(db_session):
    response = db_session.query(Block.who, Block.amount, Block.to_whom, Block.block_hash,
                                Block.number_id).select_from(Block).order_by(desc(Block.number_id)).limit(1).all()
    return {"name": response[0][0], "amount": response[0][1], "to whom": response[0][2], "block_hash": response[0][3]}, response[0][4]


def is_database_empty(db_session):
    return db_session.query(count(Block.number_id)).all()[0][0] == 0


def get_block_id(db_session, name):
    return db_session.query(Block.number_id).where(Block.who == name).all()[0][0]


def get_average_time(count_blocks: int):
    db_session = create_session()
    last_id = db_session.query(Timer.n_id).select_from(
        Timer).order_by(desc(Timer.n_id)).limit(1).all()[0][0]
    sum = db_session.query(sum_string(Timer.time)).where(
        Timer.n_id >= last_id - count_blocks + 1).all()[0][0]
    db_session.close()
    return count_blocks, sum / count_blocks


def add_time(name, time):
    db_session = create_session()
    n_id = get_block_id(db_session, name)
    t = Timer(n_id, time)
    db_session.add(t)
    db_session.commit()
    db_session.close()

def clear_tables(db_session):
    db_session.query(Block).filter(Block.number_id > 1).delete()
    db_session.commit()
    db_session.query(Timer).filter(Timer.n_id > 1).delete()
    db_session.commit()
    


class Block(Base):
    __tablename__ = 'blocks'
    number_id = Column(Integer, primary_key=True)
    who = Column(String(100), nullable=True)
    amount = Column(Integer)
    to_whom = Column(String(100), nullable=True)
    block_hash = Column(String(100), nullable=True)
    Merklies_root = Column(String(100), nullable=True)
    timestrap = Column(String(100), nullable=True)
    prev_index = Column(Integer)

    def __init__(self, name1, amount, name2, hash_, root, timestamp, prev_index):
        self.who = name1
        self.amount = amount
        self.to_whom = name2
        self.block_hash = hash_
        self.Merklies_root = root
        self.timestrap = timestamp
        self.prev_index = prev_index


class Timer(Base):
    __tablename__ = 'timer'
    n_id = Column(Integer, primary_key=True)
    time = Column(Float)

    def __init__(self, n_id, time):
        self.n_id = n_id
        self.time = time

# session = create_session()
# init_db(session)
# clear_tables(session)
