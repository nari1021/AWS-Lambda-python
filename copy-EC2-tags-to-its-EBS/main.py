# 출처 :: https://rtfm.co.ua/en/aws-lambda-copy-ec2-tags-to-its-ebs-part-2-create-a-lambda-function/ 

import os
import json
import boto3

def lambda_handler(event, context):
    region = 'ap-northeast-2'
    ec2 = boto3.resource('ec2', region_name=region)
    instance_id = event["detail"]["instance-id"]
    instance = ec2.Instance(instance_id)
    
    # ID : EC2 id
    print("[DEBUG] EC2\n\t\tID: " + str(instance))
    print("\tEBS")
    
    for vol in instance.volumes.all():   
        vol_id = str(vol)

        # VOLUME : EBS Volume id
        print("VOLUME: " + str(vol))
        
        device_id = "ec2.vol.Device('" + str(vol.attachments[0]['Device']) + "')"

        # ID : EBS Volume id
        # Dev : Volume device name
        print("\t\tID: " + vol_id + "\n\t\tDev: " + device_id)
        
        role_tag = vol.create_tags(Tags=set_role_tag(vol))
        ec2_tags = vol.create_tags(Tags=copy_ec2_tags(instance))
        # Tags set:
        # 첫 번째 출력 값은 EBS에 생성한 role 태그 값
        # 두번째 출력 값은 ec2 tag 값
        print("\t\tTags set:\n\t\t\t" + str(role_tag) + "\n\t\t\t" + str(ec2_tags) + "\n")

# kubernetes ... 라는 키값이 있는지 확인하는 함수
def is_pvc(vol):
    try:
        for tag in vol.tags:
            if tag['Key'] == 'kubernetes.io/created-for/pvc/name':
                return True
            break
    except TypeError:
        return False

# EBS의 role이라는 태그를 생성해주는 함수
def set_role_tag(vol):
    device = vol.attachments[0]['Device']
    tags_list = []
    values = {}
    
    # is_pvc 함수로 특수 키 값 확인
    if is_pvc(vol):
        values['Key'] = "Role"
        values['Value'] = "PvcDisk"
        tags_list.append(values)
    # device Name = '/dev/xvda' 인지 확인
    elif device == "/dev/xvda":
        values['Key'] = "Role"
        values['Value'] = "RootDisk"
        tags_list.append(values)
    # 이도저도 아니라면
    else:
        values['Key'] = "Role"
        values['Value'] = "DataDisk"
        tags_list.append(values)
    return tags_list

# EBS에 EC2 태그 값을 똑같이 넣어주는 함수
def copy_ec2_tags(instance):
    tags_list = []

    for instance_tag in instance.tags:
        # Env 키 값 있으면 EBS에도 넣어주고,
        if instance_tag['Key'] == 'Env':
            tags_list.append(instance_tag)
        # Tier 키 값 있으면 EBS에도 넣어주고,
        elif instance_tag['Key'] == 'Tier':
            tags_list.append(instance_tag)
        # DataClass 키 값 있으면 EBS에도 넣어주고,
        elif instance_tag['Key'] == 'DataClass':
            tags_list.append(instance_tag)
        # JiraTicket 키 값 있으면 EBS에도 넣어주고,
        elif instance_tag['Key'] == 'JiraTicket':
            tags_list.append(instance_tag)
        return tags_list
        
    if __name__ == "__main__":
        lambda_handler(event, context)
        