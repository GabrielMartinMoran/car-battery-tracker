import os
from typing import List

from fastapi import FastAPI, Depends
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from src.app.services_runner import run_services
from src.config.config_provider import ConfigProvider
from src.domain.models.measure import Measure
from src.domain.services.measure_persister import MeasurePersister
from src.domain.services.measure_retriever import MeasureRetriever

from src.infrastructure.repositories.postgres.measure_pg_repository import MeasurePGRepository
from src.utils.uvicorn_detector import is_running_on_uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup_event():
    if is_running_on_uvicorn():
        # If the api is executed locally, we start the background services in this way
        run_services()


@app.get("/")
async def get():
    with open(os.path.join(ConfigProvider.API_PAGES_PATH, 'index.html'), 'r') as f:
        html = f.read()
    return HTMLResponse(html)


@app.post('/measures', status_code=status.HTTP_201_CREATED)
async def track_measure(measure: Measure, measure_repository=Depends(MeasurePGRepository)) -> dict:
    measure_persister = MeasurePersister(measure_repository)
    measure_persister.track_measure(measure)
    return {}


@app.get('/measures', status_code=status.HTTP_201_CREATED)
async def get_recent_measures(measure_repository=Depends(MeasurePGRepository)) -> List[Measure]:
    measure_persister = MeasureRetriever(measure_repository)
    measures = measure_persister.get_recent_measures()
    return measures
