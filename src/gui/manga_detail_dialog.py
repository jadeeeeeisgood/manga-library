import tkinter as tk
from tkinter import ttk
from ..utils.theme_utils import ThemeManager

class MangaDetailDialog(tk.Toplevel):
    def __init__(self, parent, manga, image_cache, auth_manager, on_favorite_toggle=None):
        super().__init__(parent)
        self.manga = manga
        self.image_cache = image_cache
        self.auth_manager = auth_manager
        self.on_favorite_toggle = on_favorite_toggle
        
        self.title(manga.get('title', ''))
        self.geometry("800x900")
        self.resizable(False, False)
        
        # Tạo gradient background
        self.create_gradient_background()
        
        # Tạo main frame
        main_frame = ttk.Frame(self, style='Card.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.create_widgets(main_frame)
        
        # Làm cho dialog trở thành modal
        self.transient(parent)
        self.grab_set()

    def create_gradient_background(self):
        self.bg_canvas = tk.Canvas(self, width=800, height=900)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        ThemeManager.create_gradient_background(self.bg_canvas, 800, 900)

    def create_widgets(self, parent):
        # Header
        header_frame = ttk.Frame(parent, padding="20")
        header_frame.pack(fill='x')
        
        # Ảnh và thông tin cơ bản
        content_frame = ttk.Frame(header_frame)
        content_frame.pack(fill='x')
        
        # Ảnh bìa bên trái
        cover_frame = ttk.Frame(content_frame, width=250, height=350)
        cover_frame.grid(row=0, column=0, padx=(0, 20))
        cover_frame.grid_propagate(False)
        
        if self.manga.get('image_url'):
            try:
                image = self.image_cache.get_image(self.manga['image_url'], size=(250, 350))
                if image:
                    image_label = ttk.Label(cover_frame, image=image)
                    image_label.image = image
                    image_label.place(relx=0.5, rely=0.5, anchor='center')
            except Exception as e:
                print(f"Error loading image: {e}")
                
        # Thông tin chính bên phải
        info_frame = ttk.Frame(content_frame)
        info_frame.grid(row=0, column=1, sticky='nsew')
        
        # Tiêu đề
        title_label = ttk.Label(info_frame, 
                              text=self.manga.get('title', ''),
                              style='Heading.TLabel',
                              wraplength=450)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Tiêu đề tiếng Nhật
        if self.manga.get('title_japanese'):
            jp_title_label = ttk.Label(info_frame,
                                     text=self.manga.get('title_japanese', ''),
                                     font=ThemeManager.FONTS['body'],
                                     foreground=ThemeManager.COLORS['text_secondary'],
                                     wraplength=450)
            jp_title_label.pack(anchor='w', pady=(0, 20))
        
        # Thông tin nhanh
        quick_info = [
            ("👤 Tác giả", 'author'),
            ("📅 Năm xuất bản", 'year'),
            ("⭐ Xếp hạng", 'rating'),
            ("📚 Số tập", 'volumes'),
            ("📖 Số chương", 'chapters')
        ]
        
        for label, key in quick_info:
            if self.manga.get(key):
                info_frame = ttk.Frame(info_frame)
                info_frame.pack(fill='x', pady=5)
                ttk.Label(info_frame,
                         text=f"{label}:",
                         font=ThemeManager.FONTS['body'],
                         foreground=ThemeManager.COLORS['text_secondary']).pack(side='left')
                ttk.Label(info_frame,
                         text=str(self.manga.get(key)),
                         font=ThemeManager.FONTS['body_bold'],
                         foreground=ThemeManager.COLORS['text']).pack(side='left', padx=(5, 0))
        
        # Trạng thái với badge màu
        status_frame = ttk.Frame(info_frame)
        status_frame.pack(fill='x', pady=10)
        
        status_badge = tk.Label(status_frame,
                              text=self.manga.get('status', ''),
                              font=ThemeManager.FONTS['body_bold'],
                              fg='white',
                              bg=ThemeManager.COLORS['primary'],
                              padx=10,
                              pady=5)
        status_badge.pack(side='left')
        
        # Nút yêu thích
        user = self.auth_manager.get_current_user()
        is_favorite = self.manga.get('id') in user.get('favorites', [])
        
        favorite_btn = ThemeManager.create_rounded_button(
            info_frame,
            text="❤️ Xóa khỏi yêu thích" if is_favorite else "🤍 Thêm vào yêu thích",
            command=self.toggle_favorite,
            style='secondary' if is_favorite else 'primary'
        )
        favorite_btn.pack(anchor='w', pady=20)
        
        # Đường kẻ phân cách
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Thể loại
        genre_frame = ttk.Frame(parent, padding="20")
        genre_frame.pack(fill='x')
        
        ttk.Label(genre_frame,
                 text="THỂ LOẠI",
                 style='Subheading.TLabel').pack(anchor='w', pady=(0, 10))
        
        genres = self.manga.get('genres', '').split(', ')
        genre_chips_frame = ttk.Frame(genre_frame)
        genre_chips_frame.pack(fill='x')
        
        row = column = 0
        for genre in genres:
            if genre:
                chip = tk.Label(genre_chips_frame,
                              text=genre,
                              font=ThemeManager.FONTS['body'],
                              fg=ThemeManager.COLORS['text'],
                              bg=ThemeManager.COLORS['background'],
                              padx=15,
                              pady=5)
                chip.grid(row=row, column=column, padx=5, pady=5)
                
                # Hiệu ứng hover cho genre chip
                chip.bind('<Enter>', lambda e, c=chip: c.config(
                    bg=ThemeManager.COLORS['primary'],
                    fg='white'
                ))
                chip.bind('<Leave>', lambda e, c=chip: c.config(
                    bg=ThemeManager.COLORS['background'],
                    fg=ThemeManager.COLORS['text']
                ))
                
                column += 1
                if column > 3:
                    column = 0
                    row += 1
        
        # Đường kẻ phân cách
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Tóm tắt
        synopsis_frame = ttk.Frame(parent, padding="20")
        synopsis_frame.pack(fill='both', expand=True)
        
        ttk.Label(synopsis_frame,
                 text="TÓM TẮT",
                 style='Subheading.TLabel').pack(anchor='w', pady=(0, 10))
        
        synopsis_text = tk.Text(synopsis_frame,
                              wrap=tk.WORD,
                              width=70,
                              height=10,
                              font=ThemeManager.FONTS['body'],
                              bg=ThemeManager.COLORS['surface'],
                              fg=ThemeManager.COLORS['text'],
                              padx=10,
                              pady=10)
        synopsis_text.pack(fill='both', expand=True)
        synopsis_text.insert('1.0', self.manga.get('synopsis', ''))
        synopsis_text.config(state='disabled')
        
        # Footer với nút điều khiển
        btn_frame = ttk.Frame(parent, padding="20")
        btn_frame.pack(fill='x')
        
        close_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="Đóng",
            command=self.destroy,
            style='secondary'
        )
        close_btn.pack(anchor='center', pady=(0, 10))

    def toggle_favorite(self):
        """Xử lý thêm/xóa khỏi danh sách yêu thích"""
        if self.on_favorite_toggle:
            self.on_favorite_toggle(self.manga.get('id'))
            self.destroy()