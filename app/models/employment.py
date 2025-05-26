from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Employment(Base):
    __tablename__ = "employments"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    company_name = Column(String, nullable=False)
    from_year = Column(Integer, nullable=False)
    to_year = Column(Integer, nullable=True)

    profile = relationship("Profile", back_populates="employments")
