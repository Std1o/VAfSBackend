from fastapi import FastAPI
from src.vafs.api import router

app = FastAPI()
app.include_router(router)