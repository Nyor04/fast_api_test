from os import getenv
from dotenv import load_dotenv
from jwt import decode, encode


load_dotenv()

secret_key = getenv("SECRET_KEY")
secret_algorithm = getenv("ALGORITHM")


def jwt_generator(data: dict) -> str:
    token: str = encode(payload=data, algorithm=secret_algorithm,key=secret_key)
    return token


def jwt_validator(token:str) -> dict:
    parsed_token: str = token.strip('"')
    data: dict = decode(parsed_token,algorithms=[secret_algorithm],key=secret_key)
    return data