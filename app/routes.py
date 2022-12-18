from fastapi import APIRouter, Response, status, HTTPException, Depends
from .models import IngestionSchema
from fastapi.encoders import jsonable_encoder
from .database import insert_data, retrieve_data
from datetime import datetime
import random
import time
import asyncio
from .security import check_authentication_header
import pytz


router = APIRouter()


""" Ingestion endpoint, 10% of request fails with code 500
    response time is random with range of 10 and 50 ms
"""


@router.post("/ingest")
async def ingest(
    data: IngestionSchema, response: Response, auth=Depends(check_authentication_header)
):
    start = time.time()
    data = jsonable_encoder(data)
    response_time = random.randrange(10, 51)
    status_code = [200, 500]
    response_code = random.choices(status_code, weights=(90, 10))
    data["respose_time"] = response_time
    data["response_code"] = response_code[0]
    data["creation_datetime"] = (
        datetime.now(pytz.timezone("Europe/Rome")).replace(tzinfo=None).isoformat()
    )
    response_data = await insert_data(data)
    if response_data:
        if response_code[0] == 200:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in database",
        )
    standard_time = time.time() - start
    await asyncio.sleep(max(response_time / 1000 - standard_time, 0))
    return {"status_code": response_code[0], "message": "Ingestion Complete"}


@router.get("/retrieve")
async def retrieve(
    date_from: datetime, date_to: datetime, auth=Depends(check_authentication_header)
):
    date_from = date_from.replace(second=0, microsecond=0, tzinfo=None)
    date_to = date_to.replace(second=59, microsecond=999999, tzinfo=None)
    found_data = await retrieve_data(date_from, date_to)
    return found_data
