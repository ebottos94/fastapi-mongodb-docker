from datetime import datetime
import pytz

print(datetime.now())
print(datetime.now(pytz.timezone("Europe/Rome")).replace(tzinfo=None).isoformat())
