import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api
import os
from azure.monitor.opentelemetry import configure_azure_monitor

# Configura azure-monitor-opentelemetry con logger_name
APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
logger_namespace = "my_app_logger" # Define el nombre de tu logger
configure_azure_monitor(
    connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING,
    logger_name=logger_namespace
)

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

# Utiliza el logger con el namespace configurado
logger = logging.getLogger(logger_namespace)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.info('Este es un mensaje de log de ejemplo')
logger.warning('logging Warning')
logger.critical('logging Critical')
logger.debug('logging debug')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, access_log=True, reload=True)
