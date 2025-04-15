import json
import os
import requests
from datetime import datetime
import time
from ..utils.path_utils import get_manga_collection_path
from ..utils.status_utils import StatusMapping

class MangaManager:
    def __init__(self):
        """Initialize the manga management system"""
        self.data_file = get_manga_collection_path()
        self.manga_collection = []
        self.load_data()

    def load_data(self):
        """Load manga data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    self.manga_collection = json.load(file)
                    # Normalize existing statuses
                    for manga in self.manga_collection:
                        manga['status'] = StatusMapping.normalize_status(manga.get('status'))
            except json.JSONDecodeError:
                self.manga_collection = []
        else:
            self.manga_collection = []

    def save_data(self):
        """Save manga data to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.manga_collection, file, ensure_ascii=False, indent=2)

    def add_manga(self, manga):
        """Add a manga to the library"""
        # Normalize status to Vietnamese
        manga['status'] = StatusMapping.normalize_status(manga.get('status'))
        
        # Create ID for new manga
        manga_id = 1
        if self.manga_collection:
            manga_id = max(int(m.get('id', 0)) for m in self.manga_collection) + 1
        
        manga['id'] = manga_id
        manga['added_date'] = datetime.now().isoformat()
        self.manga_collection.append(manga)
        self.save_data()
        return manga_id

    def update_manga(self, manga_id, updated_info):
        """Update manga information"""
        # Normalize status to Vietnamese
        updated_info['status'] = StatusMapping.normalize_status(updated_info.get('status'))
        
        for i, manga in enumerate(self.manga_collection):
            if manga.get('id') == manga_id:
                # Keep ID and add date
                updated_info['id'] = manga_id
                updated_info['added_date'] = manga.get('added_date')
                self.manga_collection[i] = updated_info
                self.save_data()
                return True
        return False

    def delete_manga(self, manga_id):
        """Delete a manga from the library"""
        for i, manga in enumerate(self.manga_collection):
            if manga.get('id') == manga_id:
                self.manga_collection.pop(i)
                self.save_data()
                return True
        return False

    def get_manga(self, manga_id):
        """Get information of a manga"""
        for manga in self.manga_collection:
            if manga.get('id') == manga_id:
                return manga
        return None

    def get_all_manga(self):
        """Get list of all manga"""
        return self.manga_collection

    def search_manga(self, keyword):
        """Search manga by keyword"""
        keyword = keyword.lower()
        return [manga for manga in self.manga_collection
                if keyword in manga.get('title', '').lower() or
                   keyword in manga.get('author', '').lower() or
                   keyword in manga.get('genres', '').lower()]

    def search_manga_by_genre(self, genre):
        """Search manga by genre"""
        genre = genre.lower()
        return [manga for manga in self.manga_collection
                if genre in manga.get('genres', '').lower()]

    def fetch_manga_from_jikan(self, query, limit=10):
        """Get manga data from Jikan API"""
        try:
            url = f"https://api.jikan.moe/v4/manga?q={query}&limit={limit}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            manga_list = []
            for item in data.get('data', []):
                manga = self._parse_jikan_manga(item)
                manga_list.append(manga)
            
            return manga_list
        except requests.exceptions.RequestException:
            return []

    def fetch_top_manga(self, limit=10):
        """Get list of top manga from Jikan API"""
        try:
            url = f"https://api.jikan.moe/v4/top/manga?limit={limit}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            manga_list = []
            for item in data.get('data', []):
                manga = self._parse_jikan_manga(item)
                manga['rank'] = item.get('rank', 'N/A')
                manga_list.append(manga)
            
            return manga_list
        except requests.exceptions.RequestException:
            return []

    def _parse_jikan_manga(self, item):
        """Parse manga data from Jikan API"""
        # Process author information
        authors = []
        for author in item.get('authors', []):
            authors.append(author.get('name', 'Không xác định'))
        
        # Process genre information
        genres = []
        for genre in item.get('genres', []):
            genres.append(genre.get('name', 'Không xác định'))
        
        # Get publication information
        published_info = item.get('published', {})
        published_from = published_info.get('from', 'Không xác định')
        published_year = "Không xác định"
        if published_from and published_from != "Không xác định":
            try:
                published_year = published_from.split('T')[0].split('-')[0]
            except (IndexError, AttributeError):
                published_year = "Không xác định"
        
        # Normalize status to Vietnamese
        api_status = item.get('status', 'Unknown')
        status = StatusMapping.normalize_status(api_status)
        
        return {
            'title': item.get('title', 'Không có tiêu đề'),
            'title_japanese': item.get('title_japanese', 'Không có tiêu đề tiếng Nhật'),
            'author': ', '.join(authors) if authors else 'Không xác định',
            'year': published_year,
            'genres': ', '.join(genres) if genres else 'Không xác định',
            'status': status,
            'volumes': item.get('volumes', 'Không xác định'),
            'chapters': item.get('chapters', 'Không xác định'),
            'synopsis': item.get('synopsis', 'Không có mô tả'),
            'image_url': item.get('images', {}).get('jpg', {}).get('image_url', ''),
            'rating': str(item.get('score', 'Chưa xếp hạng')),
            'members': item.get('members', 0),
            'favorites': item.get('favorites', 0),
            'source': 'Jikan API (MyAnimeList)',
            'url': item.get('url', '')
        }

    def get_user_favorites(self, user_favorites):
        """Get user's favorite manga list"""
        return [manga for manga in self.manga_collection
                if manga.get('id') in user_favorites]
