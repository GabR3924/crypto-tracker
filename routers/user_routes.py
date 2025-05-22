from fastapi import APIRouter, Body
from apps.login.schemas import User
from apps.login.handler import register_user, init_user_system
from apps.login.db_handler import get_all_users

router = APIRouter(prefix="/user", tags=["users"])

# Inicializar sistema de usuarios al cargar el módulo
init_user_system()

@router.post("/register")
def register_user_route(user: User = Body(...)):
    """Registrar un nuevo usuario en el sistema"""
    try:
        success = register_user(user)
        if success:
            return {
                "status": "success", 
                "message": "Usuario registrado correctamente",
                "user_email": user.email
            }
        else:
            return {
                "status": "error", 
                "message": "El correo ya está registrado"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/all")
def get_all_users_route():
    """Obtener todos los usuarios registrados"""
    try:
        users = get_all_users()
        return {
            "status": "success", 
            "data": users,
            "count": len(users) if users else 0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}