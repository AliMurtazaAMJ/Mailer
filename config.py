"""Configuration settings for Gmail Mailer Pro."""

import os

# Gmail credentials - Replace with your credentials
EMAIL = "your-email@gmail.com"
PASSWORD = "your-app-password"

# Cache settings
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "email_cache.json")
CACHE_EXPIRY = 300  # 5 minutes in seconds

# App settings
MAX_EMAILS = 20
BATCH_SIZE = 5