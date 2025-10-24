from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Translator App Transmitter")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_KEY = os.getenv("API_KEY")
    TRANSLATION_ENGINE = os.getenv("TRANSLATION_ENGINE", "gpt")

settings = Settings()
