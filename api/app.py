import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api

app = FastAPI()
app.include_router(api.router)

# Define the filter
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/api/health"

# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# healthcheck
app.get("/api/health")(lambda: {"status": "ok"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # import boto3
    import uvicorn
    # Si se ejecuta en local, coge el profile aws especificado
    uvicorn.run("app:app", host="0.0.0.0", port=5000, access_log=True,reload=True)