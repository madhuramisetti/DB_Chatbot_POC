import uvicorn
from logger import LoggerSetup
from model_setup import ModelSetup
import os

# Initialize logging
logger_setup = LoggerSetup()
logger = logging.getLogger('app_logger')

def setup_application():
    try:
        # Download model if needed
        model_setup = ModelSetup()
        model_path = model_setup.download_model()
        
        # Update environment variable for model path
        os.environ['MODEL_PATH'] = model_path
        
        logger.info("Application setup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to setup application: {str(e)}")
        raise

if __name__ == "__main__":
    setup_application()
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)