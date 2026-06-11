from sqlalchemy import Column, Integer, String, DECIMAL
from database.connection import Base

class Producto(Base):
    __tablename__ = "Productos"

    ID_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_producto = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    costo_unitario = Column(DECIMAL(10, 2), nullable=False)