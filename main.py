from datetime import date
from controller.Controller import Controller
from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from typing import Optional


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/get-range")
async def get_data(
    startdate: Optional[str] = Query(None),
    enddate: Optional[str] = Query(None)
):
    controller = Controller()
    data = controller.get_data(str(startdate), str(enddate))
    return data