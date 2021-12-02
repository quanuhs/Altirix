from sqlalchemy import Column, Integer, ForeignKey, Date, String

from Logic import Rating
from Logic.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import event


class Contract(Base):
  __tablename__ = 'contracts'

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  tenant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  name = Column(String, nullable=True)

  owner = relationship("User", back_populates="owner_contracts", uselist=False, foreign_keys="Contract.owner_id")
  tenant = relationship("User", back_populates="tenant_contracts", uselist=False, foreign_keys="Contract.tenant_id")
  provider = relationship("User", back_populates="provider_contracts", uselist=False, foreign_keys="Contract.provider_id")

  start_date = Column(Date, nullable=False)
  end_date = Column(Date, nullable=False)
  duration = Column(Integer)

  ratings = relationship("Rating", back_populates="contract", cascade="all, delete")

  owner_rated = relationship("Rating", primaryjoin="and_(Rating.target_id == Contract.owner_id, Rating.contract_id == Contract.id)", overlaps="contract,ratings")

  tenant_rated = relationship("Rating", primaryjoin="and_(Rating.target_id == Contract.tenant_id, Rating.contract_id == Contract.id)", overlaps="contract,ratings,owner_rated")

  provider_rated = relationship("Rating", primaryjoin="and_(Rating.target_id == Contract.provider_id, Rating.contract_id == Contract.id)", overlaps="contract,ratings,owner_rated,tenant_rated")


  def __init__(self, owner_id, tenant_id, provider_id, start_date, end_date):
    self.owner_id = owner_id
    self.tenant_id = tenant_id
    self.provider_id = provider_id

    self.start_date = start_date
    self.end_date = end_date

    date_time_duration = end_date - start_date
    self.duration = date_time_duration
  
 
  def rate_all(self, owner_points, tenant_points, provider_points):
    self.rate(self.owner_id, *owner_points)
    self.rate(self.tenant_id, *tenant_points)
    self.rate(self.provider_id, *provider_points)

  def rate(self, user_id, first_points, second_points):
    if user_id == self.owner_id:
      self.ratings.append(Rating(self.id, user_id, self.tenant_id, first_points))
      self.ratings.append(Rating(self.id, user_id, self.provider_id, second_points))
    
    elif user_id == self.tenant_id:
      self.ratings.append(Rating(self.id, user_id, self.owner_id, first_points))
      self.ratings.append(Rating(self.id, user_id, self.provider_id, second_points))
    
    elif user_id == self.provider_id:
      self.ratings.append(Rating(self.id, user_id, self.tenant_id, second_points))
      self.ratings.append(Rating(self.id, user_id, self.owner_id, second_points))


  def __str__(self):
    if self.name:
      return f"Contract@{self.name} - {self.duration}"
    return f"Contract@{self.id} - {self.duration}"
  
  def __repr__(self):
    return self.__str__()



@event.listens_for(Contract, 'before_insert')
def before_insert_function(mapper, connection, target):
        target.duration = (target.end_date - target.start_date).days

