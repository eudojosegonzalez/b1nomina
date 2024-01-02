# Importa la librería Passlib
import passlib
from passlib import hash

# Pide la contraseña al usuario
password = input("Introduce la contraseña: ")

# Encripta la contraseña con el algoritmo bcrypt
password_hash = hash.hashpw(password.encode("utf-8"), "bcrypt")

# Imprime la contraseña encriptada
print("La contraseña encriptada es:", password_hash)
