from pydantic import BaseModel, EmailStr

class User(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    correo: EmailStr
