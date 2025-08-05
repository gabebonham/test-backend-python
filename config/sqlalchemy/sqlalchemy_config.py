from os import getenv
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql+psycopg://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}",
    echo=True
)