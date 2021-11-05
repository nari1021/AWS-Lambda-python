import os
import boto3
from botocore import client
import logging
from enum import Enum
import json

STATE_NAME = os.environ.get('STATE_NAME', 'running')
ACTION = os.environ.get('ACTION', 'start') # change flag by event result

VALIED_TYPE = ("start", "stop")

# set logging for INFO
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):    
    # event 분기
    currnt_event = get_event_type(event)
    
    if not VALIED_TYPE:
        err_msg = "ACTION is invalidated!! Check your lambda Environment Values ..."
        logger.error(err_msg)
        return {
            'statusCode': 500,
            'body': 'Fail',
            'error': err_msg
        }
        
    client = boto3.client('ec2')
    # start Lambda function ...
    target_instances = get_instances(client, STATE_NAME)
    
    action_result = get_action_result(client, target_instances, ACTION)
    result = action_result.get("StartingInstances", None)
    if result is None:
        return {
            'statusCode': 500,
            'body': 'Fail',
            'error': 'ACTION is invalidated!! Check your lambda Environment Valiables ...'
        }
    
    logger.info(result)
    return {
        'statusCode': 200,
        'body': 'SUCCESS',
        'state': result
    }


def get_action_result(client: client, instances: list, action_type: str) -> dict:
    instance_ids = [i.get("InstanceId") for x in instances for i in x]
    if action_type == "start":
        return client.start_instances(InstanceIds=instance_ids)
    elif action_type == "stop":
        return client.stop_instances(InstanceIds=instance_ids)
    else:
        return {} 

def get_event_type(event) -> dict:
    return {'event_type': 'start'}

def get_instances(client: client, state_name: str) -> set:
    # print(type(client))
    find_instances = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoStartStop',
                'Values': ['true']
            },
            {
                'Name': 'instance-state-name',
                'Values': [state_name],
            }
        ]
    )
    return (x.get("Instances", []) for x in find_instances.get("Reservations"))
