from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import boto.cloudformation
import boto.ec2.autoscale

@dajaxice_register(method='GET')
def get_cloudformation_template(request, template_name):
    region = request.session.get('region', "")
    cloudformation = boto.cloudformation.connect_to_region(region)
    return cloudformation.get_template(template_name)["GetTemplateResponse"]["GetTemplateResult"]["TemplateBody"]

@dajaxice_register(method='GET')
def scale_group(request, name, min_size, max_size, desired_capacity):
    min_size = int(min_size)
    max_size = int(max_size)
    desired_capacity = int(desired_capacity)
    print "Going to autoscale: %s (min: %d,max: %d,des: %d)" % (name, min_size, max_size, desired_capacity);
    region = request.session.get('region', "")
    auto_scale_connection = boto.ec2.autoscale.connect_to_region(region)
    auto_scale_groups = auto_scale_connection.get_all_groups(names=[name])
    auto_scale_group = auto_scale_groups[0]
    auto_scale_group.min_size = min_size
    auto_scale_group.max_size = max_size
    auto_scale_group.desired_capacity = desired_capacity
    print auto_scale_group.update()
    return "Success"

