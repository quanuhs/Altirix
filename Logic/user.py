from sqlalchemy import Column, Integer, String

from Logic.database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  name = Column(String)

  # contracts = relationship("Contract")

  owner_contracts = relationship("Contract", back_populates="owner", foreign_keys="Contract.owner_id", order_by="desc(Contract.id)")
  
  tenant_contracts = relationship("Contract",  back_populates="tenant", foreign_keys="Contract.tenant_id", order_by="desc(Contract.id)")

  provider_contracts = relationship("Contract",  back_populates="provider", foreign_keys="Contract.provider_id")
  
  # ratings = relationship("Rating")
  rater_ratings = relationship("Rating", foreign_keys="Rating.rater_id")
  target_ratings = relationship("Rating", foreign_keys="Rating.target_id")

  owner_ratings = relationship("Rating", primaryjoin="and_(Rating.contract_id == Contract.id, Contract.owner_id == User.id, Rating.target_id == User.id)", overlaps="target_ratings", order_by="desc(Contract.id)")

  tenant_ratings = relationship("Rating", primaryjoin="and_(Rating.contract_id == Contract.id, Contract.tenant_id == User.id, Rating.target_id == User.id)", overlaps="target_ratings, owner_ratings", order_by="desc(Contract.id)")

  provider_ratings = relationship("Rating", primaryjoin="and_(Rating.contract_id == Contract.id, Contract.provider_id == User.id, Rating.target_id == User.id)", overlaps="target_ratings, owner_ratings,tenant_ratings", order_by="desc(Contract.id)")


  def rate(self, contract, first, second):
    contract.rate(self.id, first, second)

  def __init__(self, name=""):
    self.name =  name

  def __str__(self):
    return f"User@{self.id} - {self.name}"
  
  def __repr__(self):
    return self.__str__()
  