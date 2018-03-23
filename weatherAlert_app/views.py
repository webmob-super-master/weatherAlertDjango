import json
import time

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Region, City, Owner
from .utils.alert import Alert
from .utils.weather import HourlyWeather


def index(request):
    return render(request, 'index.html')

def alert(request, region):
    requested_region = get_object_or_404(Region, name=region)
    cities = City.objects.filter(region=requested_region.id)
    owners = Owner.objects.filter(region=requested_region.id)
    formatted_owners = ' '.join([owner.slack_handle for owner in owners])
    count = []
    alerts = []

    for city in cities:
        location = [city.city, city.state]
        forecast = HourlyWeather(location)
        weather = forecast.hourly()
        time.sleep(20)
        alarm = Alert(
            weather,
            location,
            requested_region.webhook,
            requested_region.name,
            formatted_owners
            )
        counts, messages = alarm.check_weather()
        count.append(counts)
        if messages != []:
            alerts.append(messages)

    for nums in count:
        if nums > 0:
            notify = Alert(
                weather,
                location[0],
                requested_region.webhook,
                requested_region.name,
                formatted_owners)
            for alert in alerts:
                for message in alert:
                    notify.send_alert(message)
            notify.notify_ops()
            break

    json_response = {
        'region': requested_region.name,
        'cities': [city.city for city in cities],
        'ops_owners': formatted_owners,
        'alerts': alerts
    }

    data = json.dumps(json_response)

    return HttpResponse(data, content_type='application/json')

def file(request):
    content = """FD22ED87E4D2FD9FC05D33FE908C9DF9

This is ATrigger.com API Verification File.
This file should be placed on the root folder of target url. This file is unique for each account in ATrigger.com
http://example.com/mySite/Task?name=joe        This file should be available at: http://example.com/ATriggerVerify.txt
http://sub.example.com/mySite/Task?name=joe    This file should be available at: http://sub.example.com/ATriggerVerify.txt
"""
    return HttpResponse(content, content_type='text/plain')

