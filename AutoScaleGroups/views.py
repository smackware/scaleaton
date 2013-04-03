import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

import boto
import boto.ec2
import boto.ec2.autoscale
import boto.cloudformation

import boto_helper

REGION='us-east-1'
REGION='eu-west-1'

def view_cloudformation_template(request, template_name):
    context = dict(request.session)
    region = request.session.get('region', REGION)
    cloudformation = boto.cloudformation.connect_to_region(region)
    context['template'] = simplejson.dumps(cloudformation.get_template(template_name)).replace("\\n", "\n").replace("\\\"",'"')
    context['template_name'] = template_name
    return render_to_response('cloudformation_template_view.html', context)

def view_cloudformation(request):
    context = dict(request.session)
    region = request.session.get('region', REGION)
    cloudformation = boto.cloudformation.connect_to_region(region)
    context['stacks'] = [ \
           stack for stack in cloudformation.list_stacks() if not stack.stack_status.startswith("DELETE_COMPLETE") \
           ]
    return render_to_response('cloudformation_view.html', context)

def view_launch_configuration(request, name=""):
    context = dict(request.session)
    region = request.session.get('region', REGION)
    auto_scale_connection = boto.ec2.autoscale.connect_to_region(region)
    try:
        launch_config = boto_helper.get_all_launch_configuraions(auto_scale_connection, names=[name])[0]
        context['launch_config'] = launch_config
        context['action'] = 'view'
        return render_to_response('launch_config.html', context)
    except IndexError:
        return HttpResponse("Error, launch config not found: %s" % (name, ))

def view_auto_scale_groups(request):
    context = dict(request.session)
    region = request.session.get('region', REGION)
    auto_scale_connection = boto.ec2.autoscale.connect_to_region(region)
    auto_scale_groups = auto_scale_connection.get_all_groups()
    context['groups'] = auto_scale_groups
    return render_to_response('groups_view.html', context)


def view_group_instances(request, group_name):
    context = dict(request.session)
    region = request.session.get('region', REGION)
    auto_scale_connection = boto.ec2.autoscale.connect_to_region(region)
    ec2_connection = boto.ec2.connect_to_region(region)
    group = auto_scale_connection.get_all_groups(names=[group_name])[0]
    boto.ec2.connect_to_region("us-east-1")
    context['group'] = group
    instances = list()
    instance_ids = [ i.instance_id for i in group.instances ]
    if not instance_ids:
            return render_to_response('group_instances_view.html', context)
    for reservation in ec2_connection.get_all_instances(instance_ids=instance_ids):
           instances.extend(reservation.instances)
    context['instances'] = instances
    return render_to_response('group_instances_view.html', context)
    
    
