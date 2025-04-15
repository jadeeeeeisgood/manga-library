import tkinter as tk
from tkinter import ttk, messagebox
from .login_window import LoginWindow
from ..utils.image_utils import ImageCache
from ..utils.status_utils import StatusMapping
from ..utils.theme_utils import ThemeManager

class MainWindow(ttk.Frame):
    def __init__(self, parent, auth_manager, manga_manager):
        print("Initializing MainWindow...")
        super().__init__(parent)
        self.parent = parent
        self.auth_manager = auth_manager
        self.manga_manager = manga_manager
        self.image_cache = ImageCache()
        
        # Cấu hình window
        parent.title("Thư viện Manga")
        self.setup_window()
        self.create_menu()
        self.create_widgets()
        self.create_context_menu()
        
        # Thiết lập theme
        ThemeManager.setup_theme()
        
        # Pack frame chính
        self.pack(expand=True, fill='both', padx=20, pady=20)
        print("MainWindow setup completed")
        
        # Hiển thị cửa sổ đăng nhập khi khởi động
        self.show_login_window()
        print("Login window displayed")

    def setup_window(self):
        """Cấu hình cửa sổ chính"""
        window_width = 1200
        window_height = 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.parent.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.parent.minsize(800, 600)
        
        # Cấu hình background và padding
        self.style = ttk.Style()
        self.style.configure('MainWindow.TFrame', background=ThemeManager.COLORS['background'])
        self.configure(style='MainWindow.TFrame', padding=10)

    def create_menu(self):
        """Tạo menu chính"""
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # Menu Tài khoản
        account_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tài khoản", menu=account_menu)
        account_menu.add_command(label="Thông tin cá nhân", command=self.show_profile)
        account_menu.add_command(label="Đổi mật khẩu", command=self.show_change_password)
        account_menu.add_separator()
        account_menu.add_command(label="Đăng xuất", command=self.logout)
        
        # Menu Manga
        manga_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Manga", menu=manga_menu)
        manga_menu.add_command(label="Thêm manga mới", command=self.show_add_manga)
        manga_menu.add_command(label="Tìm kiếm từ API", command=self.show_search_api)
        manga_menu.add_separator()
        manga_menu.add_command(label="Xem top manga", command=self.show_top_manga)
        
        # Menu Yêu thích
        favorites_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Yêu thích", menu=favorites_menu)
        favorites_menu.add_command(label="Xem danh sách yêu thích", command=self.show_favorites)
        
        # Menu Trợ giúp
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self.show_help)
        help_menu.add_command(label="Về chúng tôi", command=self.show_about)

    def create_context_menu(self):
        """Tạo menu chuột phải"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="♥ Thêm vào yêu thích", command=self.toggle_favorite_selected)
        self.context_menu.add_command(label="🗑️ Xóa khỏi thư viện", command=self.delete_selected)

    def create_widgets(self):
        """Tạo các widget chính"""
        # Frame chính với background và padding mới
        self.main_frame = ttk.Frame(self, style='Card.TFrame', padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header với style mới
        self.create_header()
        
        # Sidebar với style mới
        self.create_sidebar()
        
        # Khung hiển thị manga với style mới
        self.create_manga_display()

    def create_header(self):
        """Tạo header với style mới"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Logo và tiêu đề
        logo_label = ttk.Label(header_frame, text="📚", font=('Helvetica', 24))
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Thư viện Manga", 
                               style='Heading.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Thanh công cụ bên phải
        toolbar_frame = ttk.Frame(header_frame)
        toolbar_frame.pack(side=tk.RIGHT)
        
        # Nút Refresh với style mới
        refresh_btn = ThemeManager.create_rounded_button(
            toolbar_frame, text="🔄 Làm mới", 
            command=self.refresh_display,
            style='secondary',
            width=15
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Label người dùng với style mới
        self.user_label = ttk.Label(toolbar_frame, text="", 
                                  font=ThemeManager.FONTS['body_bold'],
                                  foreground=ThemeManager.COLORS['text'])
        self.user_label.pack(side=tk.LEFT, padx=10)

    def create_sidebar(self):
        """Tạo sidebar với style mới"""
        sidebar_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        sidebar_frame.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 20))
        
        # Tiêu đề tìm kiếm
        search_title = ttk.Label(sidebar_frame, text="TÌM KIẾM", 
                               style='Subheading.TLabel')
        search_title.pack(pady=(0, 15))
        
        # Thanh tìm kiếm với style mới
        search_frame = ttk.Frame(sidebar_frame)
        search_frame.pack(fill='x', pady=(0, 15))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                               width=25, font=ThemeManager.FONTS['body'])
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<Return>', lambda e: self.search_manga())
        
        search_btn = ThemeManager.create_rounded_button(
            search_frame, text="🔍 Tìm", 
            command=self.search_manga,
            style='primary',
            width=8
        )
        search_btn.pack(side=tk.LEFT)
        
        # Bộ lọc thể loại
        genre_frame = ttk.LabelFrame(sidebar_frame, text="THỂ LOẠI",
                                   padding="10")
        genre_frame.pack(fill='x', pady=(0, 15))
        
        self.genre_var = tk.StringVar()
        genres = ['Tất cả', 'Action', 'Adventure', 'Comedy', 'Drama', 
                 'Fantasy', 'Horror', 'Romance', 'Sci-Fi']
        genre_combo = ttk.Combobox(genre_frame, textvariable=self.genre_var,
                                 values=genres, state='readonly',
                                 font=ThemeManager.FONTS['body'])
        genre_combo.current(0)
        genre_combo.pack(fill='x')
        genre_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_by_genre())
        
        # Bộ lọc trạng thái
        status_frame = ttk.LabelFrame(sidebar_frame, text="TRẠNG THÁI",
                                    padding="10")
        status_frame.pack(fill='x')
        
        self.status_var = tk.StringVar()
        statuses = ['Tất cả'] + list(StatusMapping.get_vietnamese_statuses())
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                  values=statuses, state='readonly',
                                  font=ThemeManager.FONTS['body'])
        status_combo.current(0)
        status_combo.pack(fill='x')
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_by_status())

    def create_manga_display(self):
        """Tạo khung hiển thị manga với style mới"""
        # Frame chứa danh sách manga với style Card
        display_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tạo Treeview với style mới
        columns = ('id', 'title', 'author', 'genres', 'status', 'rating')
        self.manga_tree = ttk.Treeview(display_frame, columns=columns, 
                                     show='headings', style='Treeview')
        
        # Định nghĩa các cột với style mới
        headings = {
            'id': ('ID', 50),
            'title': ('Tiêu đề', 300),
            'author': ('Tác giả', 150),
            'genres': ('Thể loại', 200),
            'status': ('Trạng thái', 100),
            'rating': ('Xếp hạng', 80)
        }
        
        for col, (text, width) in headings.items():
            self.manga_tree.heading(col, text=text)
            self.manga_tree.column(col, width=width)
        
        # Thêm thanh cuộn với style mới
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL,
                                command=self.manga_tree.yview)
        self.manga_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.manga_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Cấu hình grid
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)
        
        # Bind sự kiện
        self.manga_tree.bind('<Double-1>', self.show_manga_details)
        self.manga_tree.bind('<Button-3>', self.show_context_menu)

    def show_context_menu(self, event):
        """Hiển thị menu chuột phải"""
        item = self.manga_tree.identify_row(event.y)
        if item:
            # Select the item under cursor
            self.manga_tree.selection_set(item)
            try:
                manga_id = self.manga_tree.item(item)['values'][0]
                manga = self.manga_manager.get_manga(manga_id)
                if manga:
                    # Update menu label based on favorite status
                    is_favorite = manga_id in self.auth_manager.get_current_user().get('favorites', [])
                    self.context_menu.entryconfig(
                        0,  # First menu item
                        label="♥ Xóa khỏi yêu thích" if is_favorite else "♥ Thêm vào yêu thích"
                    )
                    self.context_menu.post(event.x_root, event.y_root)
            except (IndexError, TypeError):
                pass

    def toggle_favorite_selected(self):
        """Thêm/xóa manga được chọn vào danh sách yêu thích"""
        selection = self.manga_tree.selection()
        if not selection:
            return
        
        manga_id = self.manga_tree.item(selection[0])['values'][0]
        user = self.auth_manager.get_current_user()
        if not user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để sử dụng tính năng này")
            return
        
        is_favorite = manga_id in user.get('favorites', [])
        success, message = self.auth_manager.update_favorites(user['id'], manga_id, not is_favorite)
        
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    def delete_selected(self):
        """Xóa manga được chọn khỏi thư viện"""
        selection = self.manga_tree.selection()
        if not selection:
            return
            
        manga_id = self.manga_tree.item(selection[0])['values'][0]
        manga = self.manga_manager.get_manga(manga_id)
        
        if manga:
            if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa '{manga['title']}' khỏi thư viện?"):
                if self.manga_manager.delete_manga(manga_id):
                    # Xóa khỏi danh sách yêu thích nếu có
                    user = self.auth_manager.get_current_user()
                    if user and manga_id in user.get('favorites', []):
                        self.auth_manager.update_favorites(user['id'], manga_id, False)
                    messagebox.showinfo("Thành công", "Đã xóa manga khỏi thư viện!")
                    self.manga_tree.delete(selection)
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa manga. Vui lòng thử lại!")

    def show_login_window(self):
        """Hiển thị cửa sổ đăng nhập"""
        login_window = LoginWindow(self.parent, self.auth_manager, self.on_login_success)
        
        # Ẩn menu khi chưa đăng nhập
        self.menubar.entryconfig("Tài khoản", state="disabled")
        self.menubar.entryconfig("Manga", state="disabled")
        self.menubar.entryconfig("Yêu thích", state="disabled")

    def on_login_success(self):
        """Xử lý sau khi đăng nhập thành công"""
        # Bật menu
        self.menubar.entryconfig("Tài khoản", state="normal")
        self.menubar.entryconfig("Manga", state="normal")
        self.menubar.entryconfig("Yêu thích", state="normal")
        
        # Cập nhật label người dùng
        user = self.auth_manager.get_current_user()
        self.user_label.config(text=f"Xin chào, {user['username']}")
        
        # Tải danh sách manga
        self.refresh_display()

    def logout(self):
        """Xử lý đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            success, message = self.auth_manager.logout()
            if success:
                self.user_label.config(text="")
                self.manga_tree.delete(*self.manga_tree.get_children())
                self.show_login_window()

    def refresh_display(self):
        """Làm mới danh sách manga"""
        # Xóa dữ liệu cũ
        self.manga_tree.delete(*self.manga_tree.get_children())
        
        # Lấy danh sách manga và hiển thị
        manga_list = self.manga_manager.get_all_manga()
        for manga in manga_list:
            self.manga_tree.insert('', 'end', values=(
                manga.get('id', ''),
                manga.get('title', ''),
                manga.get('author', ''),
                manga.get('genres', '')[:30] + ('...' if len(manga.get('genres', '')) > 30 else ''),
                manga.get('status', ''),
                manga.get('rating', '')
            ))

    def search_manga(self):
        """Tìm kiếm manga"""
        keyword = self.search_var.get().strip()
        if keyword:
            results = self.manga_manager.search_manga(keyword)
            self.update_manga_display(results)

    def filter_by_genre(self):
        """Lọc manga theo thể loại"""
        genre = self.genre_var.get()
        if genre != 'Tất cả':
            results = self.manga_manager.search_manga_by_genre(genre)
            self.update_manga_display(results)
        else:
            self.refresh_display()

    def filter_by_status(self):
        """Lọc manga theo trạng thái"""
        status = self.status_var.get()
        if status != 'Tất cả':
            results = [m for m in self.manga_manager.get_all_manga() if m.get('status') == status]
            self.update_manga_display(results)
        else:
            self.refresh_display()

    def update_manga_display(self, manga_list):
        """Cập nhật hiển thị danh sách manga"""
        self.manga_tree.delete(*self.manga_tree.get_children())
        for manga in manga_list:
            self.manga_tree.insert('', 'end', values=(
                manga.get('id', ''),
                manga.get('title', ''),
                manga.get('author', ''),
                manga.get('genres', '')[:30] + ('...' if len(manga.get('genres', '')) > 30 else ''),
                manga.get('status', ''),
                manga.get('rating', '')
            ))

    def show_manga_details(self, event):
        """Hiển thị chi tiết manga"""
        # Lấy item được chọn
        selected_item = self.manga_tree.selection()
        if not selected_item:
            return
        
        # Lấy ID manga
        manga_id = self.manga_tree.item(selected_item)['values'][0]
        manga = self.manga_manager.get_manga(manga_id)
        
        if manga:
            # Tạo cửa sổ chi tiết
            detail_window = tk.Toplevel(self)
            detail_window.title(f"Chi tiết: {manga.get('title', '')}")
            detail_window.geometry("600x800")
            
            # Frame chính
            main_frame = ttk.Frame(detail_window, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Thêm ảnh manga nếu có
            if manga.get('image_url'):
                try:
                    image = self.image_cache.get_image(manga['image_url'], size=(200, 300))
                    if image:
                        image_label = ttk.Label(main_frame, image=image)
                        image_label.image = image  # Giữ tham chiếu đến ảnh
                        image_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
                except Exception as e:
                    print(f"Error loading image: {e}")
            
            # Hiển thị thông tin
            row = 1
            for field, value in [
                ("Tiêu đề", manga.get('title', '')),
                ("Tiêu đề tiếng Nhật", manga.get('title_japanese', '')),
                ("Tác giả", manga.get('author', '')),
                ("Năm xuất bản", manga.get('year', '')),
                ("Thể loại", manga.get('genres', '')),
                ("Trạng thái", manga.get('status', '')),
                ("Số tập", manga.get('volumes', '')),
                ("Số chương", manga.get('chapters', '')),
                ("Xếp hạng", manga.get('rating', '')),
            ]:
                ttk.Label(main_frame, text=f"{field}:", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
                ttk.Label(main_frame, text=str(value), wraplength=400).grid(row=row, column=1, sticky=tk.W, pady=5)
                row += 1
            
            # Tóm tắt
            ttk.Label(main_frame, text="Tóm tắt:", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
            synopsis = tk.Text(main_frame, wrap=tk.WORD, width=50, height=10)
            synopsis.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            synopsis.insert('1.0', manga.get('synopsis', ''))
            synopsis.config(state='disabled')

            # Thêm nút Yêu thích
            favorite_button = ttk.Button(
                main_frame,
                text="♥ Thêm vào yêu thích" if manga_id not in self.auth_manager.get_current_user().get('favorites', []) else "♥ Xóa khỏi yêu thích",
                command=lambda: self.toggle_favorite(manga_id)
            )
            favorite_button.grid(row=row+1, column=0, columnspan=2, pady=20)

    def toggle_favorite(self, manga_id):
        """Thêm/xóa manga khỏi danh sách yêu thích"""
        user = self.auth_manager.get_current_user()
        if not user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để sử dụng tính năng này")
            return
        
        is_favorite = manga_id in user.get('favorites', [])
        success, message = self.auth_manager.update_favorites(user['id'], manga_id, not is_favorite)
        
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    def show_add_manga(self):
        """Hiển thị form thêm manga mới"""
        from .add_manga_dialog import AddMangaDialog
        dialog = AddMangaDialog(self, self.manga_manager)
        self.wait_window(dialog)
        # Refresh sau khi thêm manga mới
        self.refresh_display()

    def show_search_api(self):
        """Hiển thị form tìm kiếm từ API"""
        from .search_api_dialog import SearchAPIDialog
        dialog = SearchAPIDialog(self, self.manga_manager)
        self.wait_window(dialog)
        # Refresh sau khi thêm manga mới từ API
        self.refresh_display()

    def show_top_manga(self):
        """Hiển thị danh sách top manga"""
        from .top_manga_dialog import TopMangaDialog
        dialog = TopMangaDialog(self, self.manga_manager)
        self.wait_window(dialog)
        # Refresh sau khi thêm manga mới từ danh sách top
        self.refresh_display()

    def show_favorites(self):
        """Hiển thị danh sách manga yêu thích"""
        user = self.auth_manager.get_current_user()
        if not user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để xem danh sách yêu thích")
            return
        
        favorites = self.manga_manager.get_user_favorites(user.get('favorites', []))
        self.update_manga_display(favorites)

    def show_profile(self):
        """Hiển thị thông tin cá nhân"""
        from .profile_dialog import ProfileDialog
        dialog = ProfileDialog(self, self.auth_manager)
        self.wait_window(dialog)

    def show_change_password(self):
        """Hiển thị form đổi mật khẩu"""
        from .change_password_dialog import ChangePasswordDialog
        dialog = ChangePasswordDialog(self, self.auth_manager)
        self.wait_window(dialog)

    def show_help(self):
        """Hiển thị hướng dẫn sử dụng"""
        messagebox.showinfo("Hướng dẫn sử dụng", 
            "Chào mừng đến với Thư viện Manga!\n\n"
            "- Đăng nhập/Đăng ký tài khoản để bắt đầu\n"
            "- Tìm kiếm manga bằng thanh tìm kiếm\n"
            "- Lọc manga theo thể loại và trạng thái\n"
            "- Nhấp đúp vào một manga để xem chi tiết\n"
            "- Nhấp chuột phải để thêm/xóa yêu thích hoặc xóa manga\n"
            "- Theo dõi tiến độ đọc của bạn\n\n"
            "Để biết thêm thông tin chi tiết, vui lòng liên hệ hỗ trợ."
        )

    def show_about(self):
        """Hiển thị thông tin về ứng dụng"""
        messagebox.showinfo("Về chúng tôi",
            "Thư viện Manga v1.0\n\n"
            "Một ứng dụng quản lý manga đơn giản và tiện lợi.\n\n"
            "Tính năng:\n"
            "- Quản lý bộ sưu tập manga\n"
            "- Tìm kiếm và lọc manga\n"
            "- Theo dõi tiến độ đọc\n"
            "- Đồng bộ với MyAnimeList\n\n"
            "© 2024 MangaLibrary. All rights reserved."
        )
