from fastapi import FastAPI
from GeoRequest import geo

app = FastAPI()

app.include_router(geo.router)

