import os
import boto3
from botocore import client
import logging

VALIED_TYPE = ("start", "stop")

# set logging for INFO
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # event
    currnt_event = get_event_type(event)
    
    err_msg = "ACTION is invalidated!! Check your lambda Environment Values ..."
    if not VALIED_TYPE:
        logger.error(err_msg)
        return {
            'statusCode': 500,
            'body': 'Fail',
            'error': err_msg
        }
        
    client = boto3.client('ec2')
    # start Lambda function ...
    target_instances = get_instances(client)
    action_result = get_action_result(client, target_instances, currnt_event)

    start_result = action_result.get("StartingInstances")
    stop_result = action_result.get("StoppingInstances")

    if start_result:
        logger.info(start_result)
        return {
            'statusCode': 200,
            'body': 'SUCCESS',
            'state': start_result
        }
    elif stop_result:
        logger.info(stop_result)
        return {
            'statusCode': 200,
            'body': 'SUCCESS',
            'state': stop_result
        }
    else:
        logger.error(err_msg)
        return {
            'statusCode': 500,
            'body': 'Fail',
            'error': err_msg
        }

def get_event_type(event) -> dict:
    if 'start' in list(event.get("resources"))[0]:
        return 'start'
    else:
        return 'stop'

def get_instances(client: client) -> set:
    find_instances = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoStartStop',
                'Values': ['true']
            }
        ]
    )
    return (x.get("Instances", []) for x in find_instances.get("Reservations"))

def get_action_result(client: client, instances: list, action_type: str) -> dict:
    instance_ids = [i.get("InstanceId") for x in instances for i in x]
    if action_type == "start":
        return client.start_instances(InstanceIds=instance_ids)
    return client.stop_instances(InstanceIds=instance_ids)
