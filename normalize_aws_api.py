#!/usr/bin/env python3
# A quick script to normalize the AWS API into a single json file
import json
import sys, os

STANDARD_REGIONS = { "endpoints" : {
    "af-south-1" : { },
    "ap-east-1" : { },
    "ap-northeast-1" : { },
    "ap-northeast-2" : { },
    "ap-northeast-3" : { },
    "ap-south-1" : { },
    "ap-southeast-1" : { },
    "ap-southeast-2" : { },
    "ca-central-1" : { },
    "eu-central-1" : { },
    "eu-north-1" : { },
    "eu-south-1" : { },
    "eu-west-1" : { },
    "eu-west-2" : { },
    "eu-west-3" : { },
    "me-south-1" : { },
    "sa-east-1" : { },
    "us-east-1" : { },
    "us-east-2" : { },
    "us-west-1" : { },
    "us-west-2" : { },
}}

def list_service_definitions(directory):
    to_return = []

    for root, directories, files in os.walk(directory):
        for item in files:
            if "service-2.json" in item:
                to_return.append(root+"/"+item)
    
    return to_return


def import_json(service_file):
    with open(service_file, 'r') as r:
        return json.loads(''.join(r.read()))


def do_import(service_files, endpoints):
    to_return = {}
    for file in service_files:
        service_name = file.split("/")[7]
        if service_name not in to_return.keys():
            to_return[service_name] = {}

        data = import_json(file)
        api_version = data['metadata']['apiVersion']
        endpoint_prefix = data['metadata']['endpointPrefix']
        to_return[service_name][api_version] = data

        if endpoint_prefix not in endpoints['partitions'][0]['services'].keys():
            # If it isn't in endpoints.json, assume it's in all regions with the 
            # format of <endpoint_prefix>.<region>.amazonaws.com
            to_return[service_name][api_version]['endpoints'] = STANDARD_REGIONS
        else:
            to_return[service_name][api_version]['endpoints'] = endpoints['partitions'][0]['services'][endpoint_prefix]

    return to_return


def main():
    if len(sys.argv) < 2:
        print("Usage: ./normalize_aws_api.py <botocore data dir>")
        exit()

    service_files = list_service_definitions(sys.argv[1])
    endpoints = import_json(sys.argv[1]+"/endpoints.json")

    # Directory structure is /data/<service name>/<api version>/service-2.json
    apis = do_import(service_files, endpoints)

    with open('aws-api-definition.json','w') as w:
        w.write(json.dumps(apis))


if __name__ == "__main__":
    main()