import os

def get_project_root():
    """Get the root directory of the project"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_cache_dir():
    """Get the cache directory path"""
    return os.path.join(get_project_root(), "assets", "cache")

def get_data_dir():
    """Get the data directory path"""
    return os.path.join(get_project_root(), "data")

def get_manga_collection_path():
    """Get the manga collection JSON file path"""
    return os.path.join(get_data_dir(), "manga_collection.json")

def get_users_path():
    """Get the users JSON file path"""
    return os.path.join(get_data_dir(), "users.json")

def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(get_cache_dir(), exist_ok=True)
    os.makedirs(get_data_dir(), exist_ok=True)
