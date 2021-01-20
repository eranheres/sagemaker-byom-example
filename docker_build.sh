#!/bin/sh -x
# The name of our algorithm
algorithm_name=sagemaker-example

cd container

chmod +x example/train
chmod +x example/serve

account=$(aws sts get-caller-identity --query Account --output text)

region=$(aws configure get region)
#region=${region:-us-east-1}

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"
accoutfull="${account}.dkr.ecr.${region}.amazonaws.com"

# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
#$(aws ecr get-login --region ${region} --no-include-email)
#$(aws ecr get-login --region ${region} --no-include-email)
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${accountfull}

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${algorithm_name} .
docker tag ${algorithm_name} ${fullname}

docker push ${fullname}
