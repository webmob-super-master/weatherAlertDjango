import time

from .utils.alert import Alert
from .utils.weather import HourlyWeather


def run_task(requested_region, city, formatted_owners, delay_num, total_num):
    alerts = []
    time.sleep(delay_num * 15)
    location = [cities[i].city, cities[i].state]
    forecast = HourlyWeather(location)
    weather = forecast.hourly()
    alarm = Alert(
        weather,
        location[0],
        requested_region.webhook,
        requested_region.name,
        formatted_owners
    )
    count, messages = alarm.check_weather()
    if messages != [] and count > 0:
        for message in messages:
            alarm.send_alert(message)
    if delay_num == total_num - 1:
        alarm.notify_ops()