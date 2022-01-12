import logging
import os
import boto3
from botocore import client

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def script_handler(events, context):
  LOGGER.info(f"event: {events}")
  LOGGER.info(f"context: {context}")
  
  db_cluster_identifier = events.get('DBClusterIdentifier')
  client = boto3.client('rds')
  
  target_cluster_members = get_db_cluster_members(client, db_cluster_identifier)
  target_instances = get_target_instances(client, target_cluster_members)
  
  return target_instances

def get_db_cluster_members(client: client, db_cluster_identifier: str) -> set:
    target_db_cluster = client.describe_db_clusters(
      DBClusterIdentifier = db_cluster_identifier
    )
    return (x.get("DBClusterMembers") for x in target_db_cluster.get("DBClusters"))

def get_target_instances(client: client, members: list) -> dict:
    instance_ids = [i.get("DBInstanceIdentifier") for x in members for i in x]
    return instance_ids
