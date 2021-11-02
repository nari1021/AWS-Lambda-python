import os
import boto3
import botocore
import json
import logging

region = 'ap-northeast-2'
ec2 = boto3.resource('ec2', region_name=region)

# set logging for INFO
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    if turnOn() == 'success':
        return {
            'statusCode': 200,
            'body': "SUCCESS"
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps(error)
        }
    
def turnOn():
    # 태그에 AutoStartStop 키와 true 값을 가지는 인스턴스를 찾음
    instances = ec2.instances.filter(
        Filters=[{
            # 태그 이름이 다르다면 이 부분을 수정하면 된다.
            # 현재 태그이름은 AutoStartStop 이고, 값은 true 이다.
            'Name': 'tag:AutoStartStop',
            'Values': ['true']
        }]
    )
    
    # 찾은 인스턴스들을 RunningInstances 변수에 넣음
    RunningInstances = [instance.id for instance in instances]
    
    for instance in RunningInstances:
        try:
            # RunningInstances 변수에 담긴 인스턴스들을 시작 지킴
            ec2.instances.start(InstanceIds=[instance])
            print('Start Instances ID :: ' + str(instance))
        except botocore.exceptions.ClientError as error:
            logger.error(error)
            return error
        pass
    
    return 'success'
    