# Infra manifest (local-first, cloud-ready)

Local-first:
- Storage: Parquet files under data/processed/, metadata in metadata.sqlite
- DB: SQLite for metadata and indexes
- API: FastAPI local (uvicorn)

Cloud-ready (to provision later):
- EC2 t3.micro (Free Tier) for training
- S3 bucket: <your-bucket>/mercury/data/<dataset_version>/
- DynamoDB or RDS for decision registry and policy metadata
- IAM role with S3 read/write and minimal EC2 permissions

S3 paths:
- s3://<bucket>/raw/<platform>/<market_id>/<version>.parquet
- s3://<bucket>/processed/<dataset_version>/episodes.parquet
- s3://<bucket>/checkpoints/<policy_version>/

IAM minimal:
- s3:GetObject, s3:PutObject on the bucket
- ec2:DescribeInstances (if using EC2 automation)
