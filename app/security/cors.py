import os

from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("ENVIRONMENT")

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:6969",
    "https://localhost",
    "http://localhost",
    "https://jolly-still-lark.ngrok-free.app",
    os.getenv("DEV_ORIGIN"),
    os.getenv("DEV_ORIGIN2"),
    os.getenv("DEV_ORIGIN3"),
]

# TODO: DO NOT FORGET THE PROD ORIGINS G

options = {
    "headers": ["Authorization"],
    "methods": ["GET", "POST", "OPTIONS"],
    "origins": origins,
    "credentials": True,
}
