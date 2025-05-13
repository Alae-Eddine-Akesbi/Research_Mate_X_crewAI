import os
import re

# Define output path
OUTPUT_PATH = "outputs"

def sanitize_filename(filename):
    """Sanitize a filename by removing invalid characters and replacing spaces."""
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Ensure the filename is not empty
    return filename if filename else "unnamed_file"

def ensure_output_folders():
    """Ensure that output directories exist."""
    articles_path = os.path.join(OUTPUT_PATH, "articles")
    os.makedirs(articles_path, exist_ok=True)