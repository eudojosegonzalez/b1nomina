from jwt import encode, decode


# funcion que permite crear un token
def create_token(data: dict):
    token: str = encode(payload=data, key="s132f8ff43cb0172f794af8db166ddefc027a0a321a3427832ed87399ea3e0fb4", algorithm="HS256")
    return token


def validate_token (token : str) -> dict:
    data : dict = decode (token,key="secreto", algorithms=['HS256'])
    return data