from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    chat_id = Column(String(50))
    age = Column(Integer)
    weight = Column(Float)
    menus = relationship("Menu", back_populates="user")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', chat_id='%s', age='%s', weight='%s' )>" % (
                             self.name, self.fullname, self.password, self.age, self.weight)


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="menus")
    takings = relationship("Taking", back_populates="menu")

    def __repr__(self):
        return "<Menu(name='%s', user='%s')>" % (
                             self.name, self.user_id)


class Taking(Base):
    __tablename__ = 'takings'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    menu = relationship("Menu", back_populates="takings")
    datetime = Column(DateTime)
    message = Column(String)

    def __repr__(self):
        return "<Menu(name='%s', user='%s')>" % (
                             self.name, self.user_id)
