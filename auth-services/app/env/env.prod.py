# In production, all environment variables are injected by the
# CI/CD pipeline (GitHub Actions) via GitHub Secrets.
# No .env file is loaded here.

from app.config.env import EnvConfig  # noqa: F401
