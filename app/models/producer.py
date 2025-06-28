from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String(14), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    farm_name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    total_area_hectares = Column(Float, nullable=False)
    arable_area_hectares = Column(Float, nullable=False)
    vegetation_area_hectares = Column(Float, nullable=False)
    planted_crops = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Producer(id={self.id}, name='{self.name}', farm_name='{self.farm_name}')>"
