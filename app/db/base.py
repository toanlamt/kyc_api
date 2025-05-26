# app/db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import user
from app.models import profile
from app.models import contact
from app.models import address
from app.models import document
from app.models import employment
from app.models import kyc
from app.models import income
from app.models import asset
from app.models import liability
from app.models import wealth_source


