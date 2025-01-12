from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)

    def __repr__(self): # for pretty info in print 
        return f"<User(id={self.id}, balance={self.balance})>"