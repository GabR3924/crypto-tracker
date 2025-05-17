from .handler import init_user_system, register_user
from .schemas import User

def main():
    init_user_system()

    print("Formulario de registro:")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")

    user = User(nombre=nombre, apellido=apellido, telefono=telefono, correo=correo)

    if register_user(user):
        print("✅ Usuario registrado con éxito.")
    else:
        print("❌ Error: el correo ya está registrado.")

if __name__ == "__main__":
    main()
