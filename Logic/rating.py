from sqlalchemy import Column, Integer, ForeignKey

from Logic.database import Base
from sqlalchemy.orm import relationship

class Rating(Base):
  __tablename__ = 'ratings'

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  contract_id = Column(Integer, ForeignKey("contracts.id"), nullable = False)
  rater_id = Column(Integer, ForeignKey("users.id"), nullable = False)
  target_id = Column(Integer, ForeignKey("users.id"), nullable = False)
  rate = Column(Integer, nullable = False)

  rater = relationship("User", foreign_keys="Rating.rater_id", primaryjoin="User.id == Rating.rater_id", uselist = False,overlaps="owner_ratings,provider_ratings,tenant_ratings, rater_ratings, target_ratings")
  target = relationship("User", foreign_keys="Rating.target_id", primaryjoin="User.id == Rating.target_id", uselist = False, overlaps="owner_ratings,provider_ratings,tenant_ratings, rater_ratings, target_ratings")

  contract = relationship("Contract", back_populates="ratings", uselist=False)


  def __init__(self, contract_id, rater_id, target_id, rate):
    self.contract_id = contract_id
    self.rater_id = rater_id
    self.target_id = target_id
    self.rate = rate

  def __str__(self):
    return f"Rating@{self.id} - {self.contract_id}. R: {self.rater_id} | T: {self.target_id} >> {self.rate}"
  
  def __repr__(self):
    return f"{self.rate}"