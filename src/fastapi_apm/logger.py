from loguru import logger as logurulogger
import sys
import os
from dotenv import load_dotenv
# import time
# import boto3
# import watchtower

def setup_logger(config): 

    cloud_watch_config = config["CloudWatchConfig"] 
    log_level= cloud_watch_config["log_level"]

    logurulogger.remove()# Define log colors
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "{level.icon} {level:<8} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{message}"
    )


    # Load environment variables from .env.local
    load_dotenv('.env.local')

    # Get the log level from the environment
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    # print(f"Log level set to: {log_level}")

    # Initialize the logger with the log level
    logurulogger.remove()  # Remove the default handler

    # Add colored logger to stdout
    logurulogger.add(
        sys.stdout,
        format=log_format,
        level=log_level.upper(),
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    return logurulogger

config = {"CloudWatchConfig" : {"log_group_name": "", "log_stream_name" : None, "aws_region" : "us-east-1", "log_level":"INFO"}}
logger = setup_logger(config)