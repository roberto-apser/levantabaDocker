import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api
from opencensus.ext.azure.log_exporter import AzureLogHandler

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

# get it from env 
APPLICATIONINSIGHTS_CONNECTION_STRING = 'InstrumentationKey=d9301d09-de74-40ef-bfc5-2fd45048f8b4;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/;ApplicationId=e8881afb-6e91-40c4-9466-2b09af946a9b'

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING))
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
    # import boto3
    import uvicorn
    # Si se ejecuta en local, coge el profile aws especificado
    uvicorn.run("app:app", host="0.0.0.0", port=5000, access_log=True,reload=True)
