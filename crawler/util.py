from urllib.parse import urljoin, urlparse
import hashlib
import os

def normalize_url(base_url, link):
    """Generate an absolute URL from a base and relative link."""
    # return urljoin(base_url, link).rstrip('/')
    absolute_url = urljoin(base_url, link)
    parsed_url = urlparse(absolute_url)
    normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return (normalized_url)

def hash_url(url):
    """Generate a hash for a given URL to ensure uniqueness."""
    return hashlib.md5(url.encode()).hexdigest()

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)
