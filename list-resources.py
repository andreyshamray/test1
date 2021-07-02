from __future__ import division, print_function, unicode_literals
import argparse
from datetime import datetime
import json
import boto3
import botocore



def main():
    for regionname in ["eu-central-1"]:
###For All regions!!!###
#    ec2client = boto3.client('ec2')
#    regionresponse = ec2client.describe_regions()
#    for region in regionresponse["Regions"]:
#        regionname = region["RegionName"]
        ec2client = boto3.client('ec2', region_name=regionname)
        instanceresponse = ec2client.describe_instances()
        for reservation in instanceresponse["Reservations"]:
            for instance in reservation["Instances"]:
                print(instance["InstanceId"])

        ec2_client = boto3.client('ec2')
        print('VPC:')
        print('-------')
        vpc_all = ec2_client.describe_vpcs()
        for vpc in vpc_all['Vpcs'] :
            print(vpc['VpcId'])

        ec2_client = boto3.client('ec2')
        print('Subnets:')
        print('-------')
        sn_all = ec2_client.describe_subnets()
        for sn in sn_all['Subnets'] :
            print(sn['SubnetId'])
        
        client = boto3.client('elbv2')
        print('ELBv2:')
        print('-------')
        elb_all = client.describe_load_balancers()
        for elb in elb_all['LoadBalancers'] :
            print(elb['DNSName'])

#        client = boto3.client('route53')
#        paginator = client.get_paginator('list_resource_record_sets')
#        try:
#            source_zone_records = paginator.paginate(HostedZoneId='HostedZoneId')
#            for record_set in source_zone_records:
#                for record in record_set['ResourceRecordSets']:
#                    if record['Type'] == 'CNAME':
#                        print(record['Name'])
#        
#        except Exception as error:
#            print('An error occurred getting source zone records:')
#            print(str(error))
#            raise



if __name__ == "__main__":
    main()