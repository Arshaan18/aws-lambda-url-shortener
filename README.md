# AWS Lambda URL Shortener — Project 11

A fully serverless URL shortening service built on AWS Lambda, API Gateway,
and DynamoDB. No servers, no maintenance, scales automatically, costs $0 at idle.

## Live API
POST https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/shorten

GET  https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/{short_code}

## Architecture
Client → API Gateway → Lambda (Python) → DynamoDB

↓

CloudWatch Logs

## AWS Services Used
- **Lambda** — Python 3.12, serverless compute
- **API Gateway** — HTTP API, 2 routes
- **DynamoDB** — NoSQL, on-demand capacity
- **IAM** — Lambda execution role with DynamoDB access
- **CloudWatch** — Automatic logging and metrics.

## Usage

### Create a Short URL
```bash
curl -X POST https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://github.com/Arshaan18"}'
```

### Resolve a Short URL
```bash
curl https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/{short_code}
```

## Project Structure
aws-lambda-url-shortener/

├── lambda/

│   └── function.py

├── docs/

│   ├── architecture.md

│   ├── runbook.md

│   ├── decisions.md

│   └── postmortem.md

└── README.md

## Documentation
Full industrial-style documentation in /docs:
- **architecture.md** — system design and data flow
- **runbook.md** — operational procedures and troubleshooting
- **decisions.md** — Architecture Decision Records (ADRs)
- **postmortem.md** — incidents and fixes

## Key Concepts Demonstrated
- Serverless architecture (zero server management)
- Event-driven compute with Lambda
- NoSQL key-value storage with DynamoDB
- API Gateway HTTP API + Lambda proxy integration
- IAM least-privilege roles
- CloudWatch automatic monitoring
- Path parameter parsing in Lambda

## Author
**Arshaan Shaikh** — Cloud & DevOps Engineer
- GitHub: [Arshaan18](https://github.com/Arshaan18)
- LinkedIn: [arshaan-shaikh](https://linkedin.com/in/arshaan-shaikh-95b61a227)
