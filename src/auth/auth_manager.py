import json
import os
import re
from datetime import datetime
from ..utils.path_utils import get_users_path

class AuthManager:
    def __init__(self):
        """Initialize the authentication system"""
        self.users_file = get_users_path()
        self.current_user = None
        self.load_users()

    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as file:
                    self.users = json.load(file)
            except json.JSONDecodeError:
                self.users = []
        else:
            self.users = []

    def save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w', encoding='utf-8') as file:
            json.dump(self.users, file, ensure_ascii=False, indent=2)

    def register(self, username, password, email):
        """
        Register a new user
        
        Args:
            username: Username
            password: Password
            email: Email address
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate username
        if not username or len(username) < 3:
            return False, "Tên người dùng phải có ít nhất 3 ký tự"
        
        # Check username exists
        if any(user['username'] == username for user in self.users):
            return False, "Tên người dùng đã tồn tại"
        
        # Validate password
        if not password or len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
        
        # Validate email
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email or not email_pattern.match(email):
            return False, "Email không hợp lệ"
        
        # Create new user
        user_id = 1
        if self.users:
            user_id = max(user['id'] for user in self.users) + 1
            
        new_user = {
            'id': user_id,
            'username': username,
            'password': password,  # TODO: Add password hashing
            'email': email,
            'join_date': datetime.now().isoformat(),
            'favorites': []
        }
        
        self.users.append(new_user)
        self.save_users()
        
        return True, "Đăng ký thành công"

    def login(self, username, password):
        """
        Log in a user
        
        Args:
            username: Username
            password: Password
            
        Returns:
            tuple: (success: bool, message: str)
        """
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, "Đăng nhập thành công"
        return False, "Tên đăng nhập hoặc mật khẩu không đúng"

    def logout(self):
        """
        Log out the current user
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.current_user:
            self.current_user = None
            return True, "Đã đăng xuất"
        return False, "Không có người dùng đăng nhập"

    def get_current_user(self):
        """
        Get current logged in user
        
        Returns:
            dict: Current user information or None
        """
        return self.current_user

    def change_password(self, current_password, new_password):
        """
        Change user's password
        
        Args:
            current_password: Current password
            new_password: New password
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.current_user:
            return False, "Vui lòng đăng nhập"
        
        # Verify current password
        if self.current_user['password'] != current_password:
            return False, "Mật khẩu hiện tại không đúng"
        
        # Validate new password
        if not new_password or len(new_password) < 6:
            return False, "Mật khẩu mới phải có ít nhất 6 ký tự"
        
        # Update password
        for user in self.users:
            if user['id'] == self.current_user['id']:
                user['password'] = new_password
                self.current_user = user
                self.save_users()
                return True, "Đổi mật khẩu thành công"
        
        return False, "Không tìm thấy người dùng"

    def update_favorites(self, user_id, manga_id, is_add=True):
        """
        Add/remove manga from user's favorites
        
        Args:
            user_id: User ID
            manga_id: Manga ID
            is_add: True to add, False to remove
            
        Returns:
            tuple: (success: bool, message: str)
        """
        for user in self.users:
            if user['id'] == user_id:
                if 'favorites' not in user:
                    user['favorites'] = []
                
                if is_add and manga_id not in user['favorites']:
                    user['favorites'].append(manga_id)
                    if user['id'] == self.current_user['id']:
                        self.current_user = user
                    self.save_users()
                    return True, "Đã thêm vào danh sách yêu thích"
                    
                elif not is_add and manga_id in user['favorites']:
                    user['favorites'].remove(manga_id)
                    if user['id'] == self.current_user['id']:
                        self.current_user = user
                    self.save_users()
                    return True, "Đã xóa khỏi danh sách yêu thích"
                    
                return False, "Không có thay đổi"
        
        return False, "Không tìm thấy người dùng"
