import boto.ec2
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register(method='GET')
def set_region(request, name):
    request.session['region'] = name
    return simplejson.dumps({'message':'Hello World ' + repr(boto.ec2.regions())})

@dajaxice_register(method='GET')
def get_regions(request):
    data = {
        "regions": [ r.name for r in boto.ec2.regions() ],
        "current": request.session.get("region", None)
    }
    return simplejson.dumps(data)
