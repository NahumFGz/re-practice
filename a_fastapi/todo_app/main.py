from fastapi import FastAPI
from pyexpat import model

import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
