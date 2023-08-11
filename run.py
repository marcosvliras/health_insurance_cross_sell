"""Main file."""
from fastapi import FastAPI
import uvicorn
import logging
from logging import FileHandler, StreamHandler, INFO
from app.api import router


logging.basicConfig(
    level=INFO,
    format="%(levelname)s:%(asctime)s:%(message)s",
    handlers=[FileHandler("app/logs/logs.txt", "w"), StreamHandler()],
)

# initialize API
app = FastAPI(title="Prediction API", version="2.0.0")

app.include_router(router, prefix="/v2")

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, debug=True, reload=True)
