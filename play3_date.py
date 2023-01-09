from datetime import datetime
import pytz

utc_now = datetime.now().astimezone(pytz.timezone("UTC"))
print(datetime.now().astimezone(pytz.timezone('Etc/GMT-2')))
print(type(utc_now))