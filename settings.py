from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    app_port = os.getenv("APP_PORT", 8000)
    app_debug = os.getenv("APP_DEBUG", False)
    app_version = os.getenv("APP_VERSION", "1.0.0")
    app_name = os.getenv("APP_NAME", "FastAPI")
    app_description = os.getenv("APP_DESCRIPTION", "FastAPI")
    app_author = os.getenv("APP_AUTHOR", "Faggot")
    app_secret = os.getenv("APP_SECRET", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
