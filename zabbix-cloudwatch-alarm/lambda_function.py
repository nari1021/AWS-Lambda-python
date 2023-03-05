from datetime import datetime, timedelta

import boto3

client = boto3.client('cloudwatch')

# EndTime must be greater than StartTime
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=5)


def lambda_handler(event, context):
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'zabbix20230217',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/Redshift',
                        'MetricName': 'HealthStatus',
                        'Dimensions': [
                            {
                                'Name': 'ClusterIdentifier',
                                'Value': event.cluster_id
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                },
                'ReturnData': True
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy='TimestampAscending',  # 'TimestampDescending' |'TimestampAscending'
        MaxDatapoints=100800,
        LabelOptions={
            'Timezone': '+0900'
        }
    )

    print(response)

    health_status_metric_values = (response["MetricDataResults"])[
        0].get("Values")
    print("Result :: ", sum(health_status_metric_values) //
          len(health_status_metric_values))

    return {
        'statusCode': 200
    }
