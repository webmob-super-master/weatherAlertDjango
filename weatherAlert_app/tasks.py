import time

from .utils.alert import Alert
from .utils.weather import HourlyWeather


def run_task(webhook, region_name, city, state, formatted_owners, delay_num, total_num, mode='async'):
    alerts = []
    if mode == 'async':
        time.sleep(15)
    location = [city, state]
    forecast = HourlyWeather(location)
    weather = forecast.hourly()
    alarm = Alert(
        weather,
        location,
        webhook,
        region_name,
        formatted_owners
    )
    count, messages = alarm.check_weather()
    if messages != [] and count > 0:
        for message in messages:
            alarm.send_alert(message)
    if delay_num == total_num - 1:
        alarm.notify_ops()