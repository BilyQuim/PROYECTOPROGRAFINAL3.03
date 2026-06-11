from sqlalchemy import Column, Integer, String
from database.connection import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    ID_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)
    ID_rol = Column(Integer, nullable=False)
    ID_sucursal = Column(Integer, nullable=True)  