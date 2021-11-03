import os
import boto3
import botocore
import logging

region = os.environ.get('AWS_REGION')
ec2 = boto3.resource('ec2')

# set logging for INFO
logging.basicConfig(
    format = '[%(levelname)s] %(message)s',
    force=True
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    turn_on()
    return {
        'statusCode': 200,
        'body': "SUCCESS"
    }
    
def turn_on():
    instances = ec2.instances.filter(
        Filters=[{
            'Name': 'tag:AutoStartStop',
            'Values': ['true'],
        }]
    )
    
    for instance in instances:
        try:
            ec2.instances.start(InstanceIds=[instance.id])
            logger.info('Start Inscance ID :: ' + str(instance.id))
        except botocore.exceptions.ClientError as error:
            logger.error(error)
        pass
    