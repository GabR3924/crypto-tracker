from .db_handler import insert_user, create_user_table
from .schemas import User

def init_user_system():
    create_user_table()

def register_user(user: User):
    success = insert_user(user.nombre, user.apellido, user.telefono, user.correo)
    return success
