# PredictaCart - MLOps Pipeline on AWS

## Architecture
A real-time product recommendation system deployed on AWS.

## Components
- **S3**: Data lake (raw, processed, predictions, feedback)
- **SageMaker**: Real-time inference endpoint (ml.m5.large)
- **Lambda**: Data validation + feedback collection
- **SQS**: Click event queue
- **CloudFormation**: Infrastructure as Code
- **CodePipeline**: CI/CD (GitHub → CodeBuild → Deploy)
- **CloudWatch**: Monitoring dashboard

## Endpoint
- Name: `predictacart-06250320`
- Region: `us-east-1`
- Input: JSON with 15 features
- Output: Top 5 product recommendations

## Quick Start

### 1. Send a prediction
```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name predictacart-06250320 \
  --content-type application/json \
  --body '{"inputs": [[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.1,0.2,0.3,0.4,0.5,0.6]]}' \
  --region us-east-1 \
  output.json && cat output.json
```

### 2. Deploy infrastructure
```bash
aws cloudformation deploy \
  --template-file infrastructure.yaml \
  --stack-name predictacart-stack \
  --capabilities CAPABILITY_NAMED_IAM
```

### 3. Monitor
- CloudWatch Dashboard: PredictaCart-Dashboard
- Region: us-east-1

## Cost Estimate
- SageMaker ml.m5.large: ~$0.115/hour
- S3: ~$0.023/GB
- Lambda: Free tier (1M requests/month)
- CloudWatch: Free tier (10 metrics)

## Team
- Phase 1: Data Engineer - S3 + Lambda
- Phase 2: ML Engineer - SageMaker Endpoint
- Phase 3: DevOps - CloudFormation + CodePipeline
- Phase 4: ML Monitor - CloudWatch + Feedback Loop
