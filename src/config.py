from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')
}

MODEL_CONFIG = {
    'model_path': os.getenv('MODEL_PATH'),
    'embeddings_model': 'all-MiniLM-L6-v2'
}