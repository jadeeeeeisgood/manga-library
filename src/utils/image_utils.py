import os
import requests
from PIL import Image, ImageTk
import io
import hashlib
import time
from .path_utils import get_cache_dir

class ImageCache:
    def __init__(self):
        """Initialize the image cache"""
        self.cache_dir = get_cache_dir()
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def get_cache_path(self, url):
        """Create cache file path from URL"""
        filename = hashlib.md5(url.encode()).hexdigest() + '.png'
        return os.path.join(self.cache_dir, filename)

    def get_image(self, url, size=None):
        """
        Get image from cache or download if not exists
        
        Args:
            url: Image URL
            size: tuple (width, height) to resize image
            
        Returns:
            PhotoImage object or None if error
        """
        if not url:
            return None
            
        cache_path = self.get_cache_path(url)
        
        try:
            # Check cache
            if os.path.exists(cache_path):
                image = Image.open(cache_path)
            else:
                # Download image
                response = requests.get(url)
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content))
                
                # Save to cache
                image.save(cache_path)
            
            # Resize if needed
            if size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            return ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def clear_cache(self, max_age=7*24*60*60):  # 7 days
        """Clear old cache files"""
        current_time = time.time()
        
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                # Check file age
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age:
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass
