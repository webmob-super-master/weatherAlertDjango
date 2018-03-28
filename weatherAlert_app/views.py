import json
from rq import Queue

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import django_rq

from .models import Region, City, Owner
from .tasks import run_task


def index(request):
    return render(request, 'index.html')

def alert(request, region):
    requested_region = get_object_or_404(Region, name=region)
    cities = City.objects.filter(region=requested_region.id)
    owners = Owner.objects.filter(region=requested_region.id)
    formatted_owners = ' '.join([owner.slack_handle for owner in owners])
    for i in range(0, len(cities)):
        if i > 7:
            result = django_rq.enqueue(
                run_task, 
                requested_region.webhook,
                requested_region.name,
                cities[i].city,
                cities[i].state,
                formatted_owners,
                i,
                len(cities)
        )
        else:
            result = run_task( 
                requested_region.webhook,
                requested_region.name,
                cities[i].city,
                cities[i].state,
                formatted_owners,
                i,
                len(cities),
                mode='sync'
            )
    json_response = {
        'is_completed': True
    }
    data = json.dumps(json_response)
    return HttpResponse(data, content_type='application/json')
