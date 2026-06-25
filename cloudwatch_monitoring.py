import boto3
import json
import time
from datetime import datetime

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')

ENDPOINT_NAME = 'predictacart-06250320'

def send_prediction_metrics(latency, num_predictions):
    cloudwatch.put_metric_data(
        Namespace='PredictaCart',
        MetricData=[
            {
                'MetricName': 'PredictionLatency',
                'Value': latency,
                'Unit': 'Milliseconds',
                'Timestamp': datetime.utcnow()
            },
            {
                'MetricName': 'PredictionsPerMinute',
                'Value': num_predictions,
                'Unit': 'Count',
                'Timestamp': datetime.utcnow()
            }
        ]
    )

def test_and_log():
    import numpy as np
    inputs = np.random.rand(5, 15).tolist()
    payload = json.dumps({"inputs": inputs})
    
    start = time.time()
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=payload
    )
    latency = (time.time() - start) * 1000
    result = json.loads(response['Body'].read())
    
    send_prediction_metrics(latency, len(inputs))
    print(f"✅ Metrics sent! Latency: {latency:.0f}ms, Predictions: {len(inputs)}")
    return result

if __name__ == '__main__':
    print("🔄 Sending metrics to CloudWatch...")
    for i in range(3):
        test_and_log()
        time.sleep(2)
    print("✅ Done! Check CloudWatch dashboard.")
