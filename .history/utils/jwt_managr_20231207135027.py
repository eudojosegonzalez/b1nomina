from jwt import encode, decode


# funcion que permite crear un token
def create_token(data: dict):
    token: str = encode(payload=data, key="secreto", algorithm="HS256")
    return token


def validate_token (token : str) -> dict:
    data : dict = decode (token,key="secreto", algorithms=['HS256'])
    return data