#!/usr/bin/env python3

import sagemaker
import time
from sagemaker.estimator import Estimator
from sagemaker.predictor import json_serializer, json_deserializer
import boto3


try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker')['Role']['Arn']

# train
hyper_parameters = {'train-steps': 1}
instance_type = 'local'
estimator = Estimator(role=role,
                      image_uri='sagemaker-example:latest',
                      train_instance_count=1,
                      train_instance_type=instance_type,
                      image_name='sagemaker-example:latest',
                      hyperparameters=hyper_parameters)
estimator.fit('file://tmp/example-data')

# deploy
predictor = estimator.deploy(1, instance_type, wait=True)
print("completed deploy")
time.sleep(5)

# predict
predictor.serializer = json_serializer
print("running prediction")
predictor.predict({'my_info': [ "s3 location", "other things.." ]})
print("predicted")
predictor.delete_endpoint()