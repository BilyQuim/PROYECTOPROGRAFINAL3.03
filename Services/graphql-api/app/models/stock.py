from sqlalchemy import Column, Integer, ForeignKey
from database.connection import Base

class StockActual(Base):
    __tablename__ = "Stock_Actual"

    # Estructura física de las columnas en XAMPP
    ID_stock = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ID_sucursal = Column(Integer, nullable=False)
    ID_producto = Column(Integer, nullable=False)
    stock_actual = Column(Integer, nullable=False, default=0)