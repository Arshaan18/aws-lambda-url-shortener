# Runbook
## Project: AWS Lambda URL Shortener

## Standard Operations

### Create a Short URL
```bash
curl -X POST https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://your-long-url.com"}'
```
Expected response:
```json
{
  "short_code": "aB3xYz",
  "long_url": "https://your-long-url.com",
  "created_at": "2026-06-16T08:00:00",
  "message": "Short URL created successfully"
}
```

### Resolve a Short URL
```bash
curl https://v10lgi74ei.execute-api.ap-south-1.amazonaws.com/prod/{short_code}
```

### View Lambda Logs
1. AWS Console → CloudWatch → Log groups
2. Select /aws/lambda/url-shortener
3. Click latest log stream
4. Each invocation shows: event received, duration, any errors

### View DynamoDB Records
1. AWS Console → DynamoDB → Tables → url-shortener
2. Click Explore table items
3. All short URLs visible with hits counter

### Update Lambda Code
1. AWS Console → Lambda → url-shortener
2. Edit code inline in Code tab
3. Click Deploy
4. Changes live immediately — no restart needed

### Monitor Performance
1. Lambda Console → Monitor tab
2. View: Invocations, Duration, Error rate, Throttles
3. Click View CloudWatch metrics for detailed graphs

## Troubleshooting

### Error: Short URL not found
- Cause: short_code doesn't exist in DynamoDB
- Fix: Verify the short_code was created successfully via POST first
- Check: DynamoDB → Explore items → search for short_code

### Error: Internal server error (500)
- Cause: Lambda can't connect to DynamoDB
- Fix: Check IAM role has AmazonDynamoDBFullAccess attached
- Check: Lambda → Configuration → Permissions → Role

### Error: 403 Forbidden from API Gateway
- Cause: Route not configured correctly
- Fix: API Gateway → Routes → verify POST /shorten and GET /{short_code} exist
- Fix: Check integration is pointing to correct Lambda function

### Lambda timeout
- Cause: DynamoDB query taking too long
- Fix: Lambda → Configuration → General → increase timeout to 10s
- Check: DynamoDB table is in same region as Lambda (ap-south-1)
