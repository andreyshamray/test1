from __future__ import division, print_function, unicode_literals
import sys
import argparse
from datetime import datetime
import json
import boto3
import botocore

cf = boto3.client('cloudformation')

def main(args):
    stack_name = 'test1-{}'.format(args.EnvironmentName)
    'Delete stack'

    try:
        if _stack_exists(stack_name):
            print('Deleting {}'.format(stack_name))
            stack_result = cf.delete_stack(StackName=stack_name)
            print('...waiting for stack to be deleted...')
            waiter = cf.get_waiter('stack_delete_complete')
        else:
            sys.exit('Error: CFN Stuck not exists {} !!!'.format(stack_name))
        print("...waiting for stack to be deleted...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']

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


def validate_input():
    parser = argparse.ArgumentParser(description='Please specify parameters')
    parser.add_argument('--EnvironmentName',  required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = validate_input()
    main(args)