from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env.local'))

from app.config.env import EnvConfig  # noqa: E402 (must load env first)
