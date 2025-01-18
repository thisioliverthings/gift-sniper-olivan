from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean 


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    balance = Column(Integer, default=0)
    vip = Column(Boolean, default=False)
    buying_mode = Column(Integer, default=0) # 0 - all in, 1 - percent limit, 2 - stars limit
    buying_value = Column(Integer, default=0)

    def __repr__(self): # for pretty info in print 
        return f"<User(id={self.id}, balance={self.balance}, vip={self.vip})>"
    
class Invoice(Base):
    __tablename__ = 'invoices'

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, nullable=True, default=None)
    amount = Column(Integer)
    status = Column(Boolean, default=False)

    def __repr__(self): # for pretty info in print 
        return f"<Invoice(id={self.invoice_id}, message={self.message_id}, amount={self.amount})>"