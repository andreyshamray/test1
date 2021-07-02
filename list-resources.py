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

        client_vpc = boto3.client('ec2')
        print('VPC:')
        print('-------')
        vpc_all = client_vpc.describe_vpcs()
        for vpc in vpc_all['Vpcs'] :
            print(vpc['VpcId'])

        client_sb = boto3.client('ec2')
        print('Subnets:')
        print('-------')
        sn_all = client_sb.describe_subnets()
        for sn in sn_all['Subnets'] :
            print(sn['SubnetId'])
        
        client_elb = boto3.client('elbv2')
        print('ELBv2:')
        print('-------')
        elb_all = client_elb.describe_load_balancers()
        for elb in elb_all['LoadBalancers'] :
            print(elb['DNSName'])

        client_r53 = boto3.client('route53')
        zones = client_r53.list_hosted_zones_by_name()
        if not zones or len(zones['HostedZones']) == 0:
            raise Exception("Could not find DNS zone to update")
        else:
            zone_id = zones['HostedZones'][0]['Id']
            print(zone_id)
        print('Route53 records:')
        print('-------')
        route53_all = client_r53.list_resource_record_sets(HostedZoneId=zone_id)
        for route53 in route53_all['ResourceRecordSets'] :
            print(route53['Name'])
            print(route53['Type'])

if __name__ == "__main__":
    main()