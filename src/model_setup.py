from huggingface_hub import hf_hub_download
import os
from pathlib import Path
import logging

class ModelSetup:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.logger = logging.getLogger('app_logger')
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        
    def download_model(self):
        """Download the GGUF model from HuggingFace"""
        try:
            model_path = os.path.join(self.model_dir, "llama-2-7b-chat.gguf")
            
            # Skip if model already exists
            if os.path.exists(model_path):
                self.logger.info("Model already exists, skipping download")
                return model_path
            
            self.logger.info("Downloading Llama 2 model...")
            
            # Download the model
            downloaded_path = hf_hub_download(
                repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                filename="llama-2-7b-chat.Q4_K_M.gguf",  # Using Q4 quantized version for efficiency
                local_dir=self.model_dir,
                local_dir_use_symlinks=False
            )
            
            # Rename to standard name
            os.rename(downloaded_path, model_path)
            
            self.logger.info(f"Model downloaded successfully to {model_path}")
            return model_path
            
        except Exception as e:
            self.logger.error(f"Error downloading model: {str(e)}")
            raise