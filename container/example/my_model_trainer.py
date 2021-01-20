from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import time
from os import listdir
from os.path import isfile, join
from datetime import date


def train(model_dir, data_dir, train_steps):
    # loading data for training
    print("fetching data", flush=True)
    onlyfiles = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    print("I see the files in {}:{}".format(model_dir, str(onlyfiles)), flush=True)

    # run training
    print("training my model", flush=True)
    for i in range(train_steps):
        print("--> step {}".format(i))
        time.sleep(1)

    # export model
    print("exporting the model to:{}".format(model_dir))
    with open("{}/result_model.txt".format(model_dir), "w") as f:
        today = date.today()
        f.write("Exported model on {} after running {} steps".format(today.strftime("%d/%m/%Y %s"), train_steps))



def main(model_dir, data_dir, train_steps):
    train(model_dir, data_dir, train_steps)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    # For more information:
    # https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html
    args_parser.add_argument(
        '--data-dir',
        default='/opt/ml/input/data/training',
        type=str,
        help='The directory where the CIFAR-10 input data is stored. Default: /opt/ml/input/data/training. This '
             'directory corresponds to the SageMaker channel named \'training\', which was specified when creating '
             'our training job on SageMaker')

    # For more information:
    # https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html
    args_parser.add_argument(
        '--model-dir',
        default='/opt/ml/model',
        type=str,
        help='The directory where the model will be stored. Default: /opt/ml/model. This directory should contain all '
             'final model artifacts as Amazon SageMaker copies all data within this directory as a single object in '
             'compressed tar format.')

    args_parser.add_argument(
        '--train-steps',
        type=int,
        default=100,
        help='The number of steps to use for training.')
    args = args_parser.parse_args()
    main(**vars(args))
