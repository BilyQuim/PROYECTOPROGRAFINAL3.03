from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt
from datetime import datetime, timedelta, timezone

from database.connection import get_db
from models.usuario import Usuario

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

# VALIDACIÓN CON PYDANTIC
class LoginSchema(BaseModel):
    nombre_usuario: str = Field(..., description="Nombre de usuario registrado")
    contraseña: str = Field(..., description="Contraseña plana de acceso")

# ENDPOINT DE LOGICAL LOGIN 
@router.post("/login")
def iniciar_sesion(payload: LoginSchema, db: Session = Depends(get_db)):
    # Ejecutamos la consulta apuntando a la tabla 'usuarios'
    sql = text("SELECT ID_usuario, contraseña, ID_rol, ID_sucursal FROM usuarios WHERE nombre_usuario = :u")
    result = db.execute(sql, {"u": payload.nombre_usuario}).fetchone()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El nombre de usuario o la contraseña son incorrectos"
        )
    
    user_data = dict(result._mapping)
    
    if user_data["contraseña"] != payload.contraseña:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El nombre de usuario o la contraseña son incorrectos"
        )
    tiempo_expiracion = datetime.now(timezone.utc) + timedelta(hours=2)
    
    token_payload = {
        "sub": user_data["ID_usuario"],                 
        "username": payload.nombre_usuario,
        "role": user_data["ID_rol"],                
        "sucursal": user_data["ID_sucursal"],            
        "exp": tiempo_expiracion        
    }
    
    # EMISIÓN DEL TOKEN
    token_firmado = jwt.encode(token_payload, "SECRET_KEY", algorithm="HS256")
    
    return {
        "access_token": token_firmado,
        "token_type": "bearer",
        "expires_in": "2 horas"
    }