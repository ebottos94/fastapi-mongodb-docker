import motor.motor_asyncio
from datetime import datetime
from decouple import config

USER_MONGO = config("MONGO_USERNAME")
PASSWORD_MONGO = config("MONGO_PASSWORD")

MONGO_DETAILS = f"mongodb://{USER_MONGO}:{PASSWORD_MONGO}@mongodb/?authSource=admin"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.logs

log_collection = database.get_collection("logs_collection")


async def insert_data(data: dict):
    try:
        log_collection.insert_one(data)
        return True
    except:
        return False


async def retrieve_data(date_from: datetime, date_to: datetime):
    found_data = []
    data = 0
    statistics = inizialize_statistics()
    result = {"values": [], "logs": []}
    n = 0
    async for found in log_collection.find(
        {
            "creation_datetime": {
                "$gte": date_from.isoformat(),
                "$lte": date_to.isoformat(),
            }
        },
        {"_id": 0},
    ).sort("creation_datetime"):
        # first iteration
        if data == 0:
            data = datetime.fromisoformat(found["creation_datetime"]).replace(
                second=0, microsecond=0, tzinfo=None
            )
            statistics = update_statistics(statistics, data, found)
            found_data.append(found)
        else:
            # same creation minute
            if data == datetime.fromisoformat(found["creation_datetime"]).replace(
                second=0, microsecond=0, tzinfo=None
            ):
                statistics = update_statistics(statistics, data, found)
                found_data.append(found)
            else:
                for i in statistics:
                    if i["creation_datetime"] != "":
                        result["values"].append(i)
                data = datetime.fromisoformat(found["creation_datetime"]).replace(
                    second=0, microsecond=0, tzinfo=None
                )
                statistics = inizialize_statistics()
                statistics = update_statistics(statistics, data, found)
                found_data = []
                found_data.append(found)
    for i in statistics:
        if i["creation_datetime"] != "":
            result["values"].append(i)
    if len(found_data) > 10:
        result["logs"] = found_data[-10:]
    else:
        result["logs"] = found_data
    return result


def update_statistics(statistics, data, log):
    if statistics[log["key"] - 1]["creation_datetime"] == "":
        statistics[log["key"] - 1]["creation_datetime"] = data
    statistics[log["key"] - 1]["total_response_time_ms"] += log["respose_time"]
    statistics[log["key"] - 1]["total_requests"] += 1
    if log["response_code"] == 500:
        statistics[log["key"] - 1]["total_errors"] += 1
    return statistics


def inizialize_statistics():
    statistics = [
        {
            "key": 1,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
        {
            "key": 2,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
        {
            "key": 3,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
        {
            "key": 4,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
        {
            "key": 5,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
        {
            "key": 6,
            "creation_datetime": "",
            "total_response_time_ms": 0,
            "total_requests": 0,
            "total_errors": 0,
        },
    ]

    return statistics
