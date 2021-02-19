#!/usr/bin/env python

import sys
import json

REQUIRED_TAGS = (
    'aws:cloudformation:stack-name',
    'aws:cloudformation:stack-id',
    'aws:cloudformation:logical-id'
)

print('\nSEARCHING FOR THESE TAGS:\n')
for tag in REQUIRED_TAGS:
    print(tag)

raw_data = ''
for line in sys.stdin:
    raw_data += line

data = json.loads(raw_data)

untagged_resources = []
noncompliant_resources = []
compliant_resources = []
for resource in data['ResourceTagMappingList']:
    if len(resource['Tags']) == 0:
        untagged_resources.append(resource)
        continue
    tags = [t['Key'] for t in resource['Tags']]
    is_compliant = all(t in tags for t in REQUIRED_TAGS)
    if is_compliant:
        compliant_resources.append(resource)
    else:
        noncompliant_resources.append(resource)

print('\nRESOURCES WITH NO TAGS:\n')
for resource in untagged_resources:
    print(resource['ResourceARN'])

print('\nRESOURCES WITH NON-COMPLIANT TAGS:\n')
for resource in noncompliant_resources:
    print(resource['ResourceARN'])
    for tag in resource['Tags']:
        print('   - {0} = {1}'.format(tag['Key'], tag['Value']))

print('\nRESOURCES WITH COMPLIANT TAGS:\n')
for resource in compliant_resources:
    print(resource['ResourceARN'])
print('')
