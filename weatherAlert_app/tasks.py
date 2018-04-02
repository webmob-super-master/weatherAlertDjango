import time

from django.core.cache import cache

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
        cache.set('requires_notify', 1)
        for message in messages:
            alarm.send_alert(message)
    requires_notify = cache.get('requires_notify')
    if (delay_num == total_num - 1) and (requires_notify == 1):
        alarm.notify_ops()