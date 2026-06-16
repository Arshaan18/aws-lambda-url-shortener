# Post-Mortem / Challenges Log
## Project: AWS Lambda URL Shortener

## Incident 001: GET endpoint returning "Short URL not found"

**Date:** 2026-06-16
**Severity:** Medium
**Duration:** ~10 minutes

**What happened:**
After creating a short URL via POST /shorten successfully, the GET
/{short_code} endpoint consistently returned "Short URL not found"
even though the item existed in DynamoDB.

**Root Cause:**
API Gateway HTTP API with a stage named "prod" prepends the stage name
to the rawPath. So when calling /prod/aU9PeI, the Lambda received
rawPath = "/prod/aU9PeI". The code was doing path.strip('/') which
returned "prod/aU9PeI" — not matching the short_code "aU9PeI" in DynamoDB.

**Fix Applied:**
Changed path parsing from:
```python
short_code = path.strip('/')
```
To:
```python
short_code = path.strip('/').split('/')[-1]
```
This extracts only the last segment of the path regardless of prefix.

**Prevention:**
When using API Gateway with named stages, always extract path parameters
using pathParameters from the event object instead of parsing rawPath manually.
Production fix would use:
```python
short_code = event.get('pathParameters', {}).get('short_code', '')
```

---

## Incident 002: Lambda Permissions Error (anticipated)

**What could happen:**
Lambda returns 500 error with "AccessDeniedException" when trying to
write to DynamoDB.

**Root Cause:**
Lambda execution role missing DynamoDB permissions.

**Fix:**
IAM → Roles → url-shortener-role → Add AmazonDynamoDBFullAccess policy.

**Prevention:**
In production, use a custom IAM policy scoped to only the specific
DynamoDB table and only the required actions (PutItem, GetItem, UpdateItem).
Never use FullAccess policies in production — principle of least privilege.
