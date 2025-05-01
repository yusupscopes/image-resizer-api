import boto3

cloudwatch = boto3.client('cloudwatch')

def publish_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='ImageResizerAPI',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit
            },
        ]
    )