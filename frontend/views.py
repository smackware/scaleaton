import simplejson

def set_region(request, name):
    request.session['region'] = name
    return simplejson.dumps({'message':'Hello World ' + repr(boto.ec2.regions())})

def get_regions(request):
    data = {
        "regions": [ r.name for r in boto.ec2.regions() ],
        "current": request.session.get("region", None)
    }
    return simplejson.dumps(data)


