from __future__ import division, print_function, unicode_literals
import argparse
from datetime import datetime
import json
import boto3
import botocore

cf = boto3.client('cloudformation')

def main(args):
    stack_name = 'test1-{}'.format(args.EnvironmentName)
    'Update or create stack'
    template = 'vpc-elb.template'

    template_data = _parse_template(template)

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Capabilities': ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        'Parameters': [
            {
                'ParameterKey': 'EnvironmentName',
                'ParameterValue': args.EnvironmentName
            },
            {
                'ParameterKey': 'DeployELB',
                'ParameterValue': args.DeployELB
            }
        ],
        'Tags': [
            {
                'Key': 'Product',
                'Value': 'Test1'
            },
            {
                'Key': 'Team',
                'Value': 'DevOps'
            },
            {
                'Key': 'Contact',
                'Value': 'devops.dev@my-test1-app.com'
            }
        ]
        #'EnableTerminationProtection': "True"
    }

    try:
        if _stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            stack_result = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    stack = cf.describe_stacks(StackName=stack_name)
    # print(json.dumps(
    #     stack,
    #     indent=2,
    #     default=json_serial
    # ))
    stackOutputs = dict((i["OutputKey"], i["OutputValue"]) for i in stack['Stacks'][0]['Outputs'])


def _parse_template(template):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


def _parse_parameters(parameters):
    with open(parameters) as parameter_fileobj:
        parameter_data = json.load(parameter_fileobj)
    return parameter_data


def _stack_exists(stack_name):
    try:
        stack = cf.describe_stacks(StackName=stack_name)
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'ValidationError' and err.response['Error']['Message'].endswith("does not exist"):
            return False
        raise

    if stack['Stacks'][0]['StackStatus'] == 'DELETE_COMPLETE':
        return False

    return True

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

def validate_input():
    parser = argparse.ArgumentParser(description='Please specify parameters')
    parser.add_argument('--EnvironmentName',  required=True)
    parser.add_argument('--DeployELB', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = validate_input()
    main(args)