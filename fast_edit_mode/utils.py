# utils.py

import os
import yaml
import logging
from dotenv import load_dotenv

def load_config(config_path='config.yaml'):
    load_dotenv()  # Load environment variables from .env
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    # Add environment variables to config
    config['api_keys'] = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'huggingface': os.getenv('HUGGINGFACE_API_KEY'),
    }
    return config

def setup_logging(config):
    logging.basicConfig(
        level=getattr(logging, config['logging']['level'].upper(), 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config['logging'].get('file', 'fast_edit_mode.log'),
        filemode='a',
    )
