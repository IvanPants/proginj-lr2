from fastapi import FastAPI
from config import engine
import models
from routers import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="first server",
    description="1 try",
    docs_url="/"
)


app.include_router(router, prefix="/user", tags=["user"])

