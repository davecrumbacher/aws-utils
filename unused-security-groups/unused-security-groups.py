'''

unused-security-groups.py: List security groups within a region that 
are not associated with any EC2 instances

This script looks for an AWS key pair using environment variables 
AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. The region defaults to 
us-east-1, but can set using environment variable AWS_REGION.

The output lists the unused security groups by name and security 
group ID.

Requires boto3 and tabulate packages. Or run this:

    pip install -r requirements.txt

'''

import os
import sys
import boto3
from tabulate import tabulate

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

ec2 = boto3.client('ec2',
                    region_name=AWS_REGION,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

response = ec2.describe_instances()
instances = {}
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        for group in instance['SecurityGroups']:
            group_id = group['GroupId']
            if group_id not in instances:
                instances[group_id] = set()
            instances[group_id].add(instance_id)

response = ec2.describe_security_groups()
sg = {}
for group in response['SecurityGroups']:
    sg[group['GroupId']] = group['GroupName']

print('\nUnused security groups in {0}:\n'.format(AWS_REGION))
rows = []
for sg_id in sg:
    if sg_id in instances:
        continue
    rows.append([sg[sg_id], sg_id])
print(tabulate(rows, headers=['SG Name', 'SG ID']) + '\n')
