
#! /bin/bash
set -e

npm run --prefix 'web' build

# build image
docker-compose build

# push image to ECR repo
export AWS_DEFAULT_REGION=us-east-1
aws ecr get-login-password | docker login --username AWS --password-stdin 953143184104.dkr.ecr.us-east-1.amazonaws.com
docker-compose push

# # deploy image and env vars
fargate service deploy -f docker-compose.yml
