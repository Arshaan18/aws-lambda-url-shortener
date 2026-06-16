# Architecture Document
## Project: AWS Lambda URL Shortener

## Overview
A fully serverless URL shortening service built on AWS. No servers to manage,
scales automatically, and costs nothing at idle.

## Architecture Diagram
Client (curl/browser)

↓

API Gateway (HTTP API)

POST /shorten → Lambda

  GET /{short_code} → Lambda

↓

Lambda Function (Python 3.12)

Generates short codes
Reads/writes DynamoDB
Returns JSON responses

      ↓

DynamoDB (NoSQL)
Table: url-shortener
Partition key: short_code
Stores: long_url, hits, created_at

↓

CloudWatch Logs (automatic)
Every Lambda invocation logged
Duration, memory, errors tracked


## Components

### API Gateway
- Type: HTTP API (cheaper and faster than REST API)
- Stage: prod
- Routes:
  - POST /shorten — creates a short URL
  - GET /{short_code} — resolves a short URL
- Auto-deploys on change

### Lambda Function
- Name: url-shortener
- Runtime: Python 3.12
- Memory: 128MB
- Timeout: 3 seconds (default)
- Trigger: API Gateway HTTP API
- IAM Role: AmazonDynamoDBFullAccess

### DynamoDB
- Table: url-shortener
- Partition key: short_code (String)
- Capacity mode: On-demand
- No provisioned throughput needed

### CloudWatch
- Log group: /aws/lambda/url-shortener
- Automatic logging of all invocations
- Metrics: Duration, Errors, Invocations, Throttles

## Data Flow

### Creating a Short URL (POST /shorten)
1. Client sends POST with long_url in body
2. API Gateway receives request, triggers Lambda
3. Lambda generates 6-char alphanumeric short_code
4. Lambda writes item to DynamoDB
5. Lambda returns short_code + metadata as JSON

### Resolving a Short URL (GET /{short_code})
1. Client sends GET with short_code in path
2. API Gateway triggers Lambda with path parameter
3. Lambda extracts short_code from path
4. Lambda queries DynamoDB by partition key
5. Lambda increments hit counter
6. Lambda returns long_url + metadata as JSON

## Cost Analysis
| Service | Free Tier | Estimated Usage | Cost |
|---------|-----------|-----------------|------|
| Lambda | 1M requests/month | ~100/month | $0 |
| API Gateway | 1M calls/month | ~100/month | $0 |
| DynamoDB | 25GB + 25 RCU/WCU | <1MB | $0 |
| CloudWatch | 5GB logs/month | <1MB | $0 |
| **Total** | | | **$0** |
