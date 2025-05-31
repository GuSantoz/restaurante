from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from abc import ABCMeta
import warnings

# Oculta todos os avisos de tipo Warning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning)

from sqlalchemy.exc import SAWarning
warnings.filterwarnings("ignore", category=SAWarning)
warnings.filterwarnings("ignore", message=".*LegacyAPIWarning.*")

class BaseMeta(DeclarativeMeta, ABCMeta):
    pass

Base = declarative_base(metaclass=BaseMeta)

db = create_engine("sqlite:///restaurante.db", echo=False)
Session = sessionmaker(bind=db)
session = Session()