from datetime import datetime

import uvicorn
from fastapi import FastAPI

from api.routes.patients import patients_router

app = FastAPI()


def run():
    uvicorn.run(app, host="localhost", port=8000)


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
def root():
    return {"message": "FastAPI Service is running"}


app.include_router(patients_router)


if __name__ == "__main__":
    run()
