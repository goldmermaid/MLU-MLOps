import train
import argparse
import sys
import os
import traceback
from sagemaker_inference import model_server
from sagemaker_training import environment

if __name__ == "__main__":
    if len(sys.argv) < 2 or ( not sys.argv[1] in [ "serve", "train" ] ):
        raise Exception("Invalid argument: you must inform 'train' for training mode or 'serve' predicting mode") 
        
    if sys.argv[1] == "train":
        
        env = environment.Environment()
        
        parser = argparse.ArgumentParser()
        # https://github.com/aws/sagemaker-training-toolkit/blob/master/ENVIRONMENT_VARIABLES.md
        parser.add_argument("--max-depth", type=int, default=10)
        parser.add_argument("--n-jobs", type=int, default=env.num_cpus)
        parser.add_argument("--n-estimators", type=int, default=120)
        
        # reads input channels training and testing from the environment variables
        parser.add_argument("--train", type=str, default=env.channel_input_dirs["train"])
        parser.add_argument("--validation", type=str, default=env.channel_input_dirs["validation"])

        parser.add_argument("--model-dir", type=str, default=env.model_dir)
        
        args,unknown = parser.parse_known_args()
        train.start(args)
    else:
        model_server.start_model_server(handler_service="serving.handler")
