import os
import boto3
from botocore import client
import logging
import ast

# set logging for INFO
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    client = boto3.client('ec2')
    
    # start Lambda function ...
    target_instances = get_instances(client)
    make_tags(client, target_instances)
    
def get_instances(client: client) -> set:
    find_instances = client.describe_instances()
    return (x.get("Instances", []) for x in find_instances.get("Reservations"))

# Env 키값이 있는지 확인하는 함수
def check_tags(item, tag_name) -> bool:
    try:
        for tag in item:
            if tag['Key'] == tag_name:
                print('True')
                return True
            # print(tag['Key'] + '\n')
    except TypeError:
        return False
        
def make_tags(client: client, instances: list) -> dict:
    for x in instances:
        for i in x:
            print(i)
            item = i.get("InstanceId")
            item_tags = i.get("Tags")
            
            if not check_tags(item_tags, 'Env'):
                client.create_tags(
                    Resources=[item],
                    Tags = [
                        {
                            'Key': 'Env',
                            'Value': 'env'
                        }
                    ]
                )

                