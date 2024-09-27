import logging
import os

from pydantic import BaseModel

logger = logging.getLogger(__name__)
project_dir: str = os.path.abspath(os.path.join(__file__, "../.."))



class Settings(BaseModel):
    appname: str = "Mistral Chatbot API Server"
    project_dir: str = project_dir


settings = Settings()
