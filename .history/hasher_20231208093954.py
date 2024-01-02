from passlib.hash import bcrypt

def hash_password(password):
  hasher = bcrypt.Hasher()
  hash = hasher.hash(password)
  return hash

def verify_password(password, hash):
  hasher = bcrypt.Hasher()
  is_valid = hasher.verify(password, hash)
  return is_valid

def main():
  password = input("Introduce una contraseña: ")
  hash = hash_password(password)
  print("La contraseña hash es:", hash)

  password2 = input("Introduce otra contraseña: ")
  is_equal = verify_password(password2, hash)
  if is_equal:
    print("Las contraseñas son iguales")
  else:
    print("Las contraseñas son diferentes")
