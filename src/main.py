from datetime import datetime

import uvicorn
from fastapi import FastAPI

app = FastAPI()


def run():
    uvicorn.run(app, host="localhost", port=8000)


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
def root():
    return {"message": "FastAPI Service is running"}


if __name__ == "__main__":
    run()
