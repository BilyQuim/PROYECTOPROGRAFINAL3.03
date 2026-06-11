from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt

from database.connection import get_db
from models.producto import Producto

router = APIRouter(prefix="/api/v1/rest", tags=["Productos"])

# Inicialiación de seguidad JWT
security = HTTPBearer()

# Verificación de datos de entrada con Pydantic
class ProductoBaseSchema(BaseModel):
    nombre_producto: str = Field(..., max_length=100, description="Nombre de la vela o incienso")
    categoria: str = Field(..., max_length=50, description="Categoría comercial")
    costo_unitario: float = Field(..., ge=0.0, description="Costo unitario mayor o igual a 0")

class ProductoResponseSchema(ProductoBaseSchema):
    ID_producto: int

    class Config:
        from_attributes = True


# Funcion de verificación de token JWT 
def verificar_token_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        return payload 
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado o alterado"
        )


# CRUD DE PRODUCTOS (Protegidos por JWT)

# Registrar un producto nuevo
@router.post("/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(p: ProductoBaseSchema, db: Session = Depends(get_db), usuario=Depends(verificar_token_jwt)):
    sql = text("INSERT INTO productos (nombre_producto, categoria, costo_unitario) VALUES (:n, :c, :cu)")
    db.execute(sql, {"n": p.nombre_producto, "c": p.categoria, "cu": p.costo_unitario})
    db.commit()
    return {"message": "Producto guardado con éxito en la base de datos de Docker"}


# Listar todos los productos
@router.get("/productos", response_model=list[ProductoResponseSchema])
def listar_productos(db: Session = Depends(get_db)):
    sql = text("SELECT ID_producto, nombre_producto, categoria, costo_unitario FROM productos")
    result = db.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]


# Modificar un producto existente 
@router.put("/productos/{id}")
def actualizar_producto(id: int, p: ProductoBaseSchema, db: Session = Depends(get_db), usuario=Depends(verificar_token_jwt)):
    verificar = db.execute(text("SELECT ID_producto FROM productos WHERE ID_producto = :id"), {"id": id}).fetchone()
    if not verificar:
        raise HTTPException(status_code=404, detail=f"Error: El producto con ID {id} no existe en la base de datos")
    
    sql = text("UPDATE productos SET nombre_producto = :n, categoria = :c, costo_unitario = :cu WHERE ID_producto = :id")
    db.execute(sql, {"n": p.nombre_producto, "c": p.categoria, "cu": p.costo_unitario, "id": id})
    db.commit()
    return {"message": f"Producto con ID {id} actualizado correctamente"}


# Eliminar un producto 
@router.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db), usuario=Depends(verificar_token_jwt)):
    verificar = db.execute(text("SELECT ID_producto FROM productos WHERE ID_producto = :id"), {"id": id}).fetchone()
    if not verificar:
        raise HTTPException(status_code=404, detail=f"Error: No se puede eliminar. El producto con ID {id} no existe")
    
    sql = text("DELETE FROM productos WHERE ID_producto = :id")
    db.execute(sql, {"id": id})
    db.commit()
    return {"message": f"Producto con ID {id} eliminado con éxito"}