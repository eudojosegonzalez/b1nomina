# Importa la librería Passlib
import passlib.hash

# Pide la contraseña al usuario
password = input("Introduce la contraseña: ")

# Encripta la contraseña con el algoritmo bcrypt
password_hash = passlib.hash.hashpw(password.encode("utf-8"), "bcrypt")

# Imprime la contraseña encriptada
print("La contraseña encriptada es:", password_hash)
