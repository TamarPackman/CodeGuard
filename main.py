from fastapi import FastAPI
from routers import analyze, alerts

app = FastAPI()

app.include_router(analyze.router)
app.include_router(alerts.router)