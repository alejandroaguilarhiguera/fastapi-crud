import os

from dotenv import load_dotenv
from app.config.database import Base
from app import models

load_dotenv()

config.set_main_option(
    "sqlalchemy.url",
    os.environ["SQLALCHEMY_DATABASE_URI"].replace("%", "%%"),
)

target_metadata = Base.metadata