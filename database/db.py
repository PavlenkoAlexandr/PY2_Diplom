import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import settings

Base = declarative_base()

engine = sq.create_engine(
    f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:5432/{settings.DB_NAME}'
)
Session = sessionmaker(bind=engine)


class Vkuser(Base):

    __tablename__ = 'vkuser'

    # id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, primary_key=True)
    birthdate = sq.Column(sq.String)
    sex = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    white_ids = relationship('Whitelist', uselist=False)
    black_ids = relationship('Blacklist', uselist=False)


class Whitelist(Base):

    __tablename__ = 'whitelist'

    id = sq.Column(sq.Integer, primary_key=True)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('vkuser.vk_id'))
    pair_id = sq.Column(sq.Integer)
    photos = sq.Column(sq.String)
    full_name = sq.Column(sq.String)
    url = sq.Column(sq.String)

class Blacklist(Base):

    __tablename__ = 'blacklist'

    id = sq.Column(sq.Integer, primary_key=True)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('vkuser.vk_id'))
    pair_id = sq.Column(sq.Integer)
