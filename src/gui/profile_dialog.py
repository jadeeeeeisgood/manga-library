import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..utils.theme_utils import ThemeManager

class ProfileDialog(tk.Toplevel):
    def __init__(self, parent, auth_manager):
        super().__init__(parent)
        self.auth_manager = auth_manager
        
        self.title("Thông tin cá nhân")
        self.geometry("500x600")
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
        self.bg_canvas = tk.Canvas(self, width=500, height=600)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        ThemeManager.create_gradient_background(self.bg_canvas, 500, 600)

    def create_widgets(self, parent):
        # Lấy thông tin người dùng hiện tại
        user = self.auth_manager.get_current_user()
        if not user:
            return
        
        # Header
        header_frame = ttk.Frame(parent, padding="20")
        header_frame.pack(fill='x')
        
        # Avatar và tiêu đề
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='center', pady=(0, 20))
        
        logo_label = ttk.Label(title_frame, text="👤", font=('Helvetica', 48))
        logo_label.pack(pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                              text="Thông Tin Cá Nhân",
                              style='Heading.TLabel')
        title_label.pack()
        
        # Đường kẻ phân cách
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=20)
        
        # Form frame
        form_frame = ttk.Frame(parent, padding="20")
        form_frame.pack(fill='both', expand=True)
        
        # Style cho labels
        heading_style = {'font': ThemeManager.FONTS['subheading'],
                       'foreground': ThemeManager.COLORS['text']}
        label_style = {'font': ThemeManager.FONTS['body'],
                      'foreground': ThemeManager.COLORS['text_secondary']}
        value_style = {'font': ThemeManager.FONTS['body_bold'],
                      'foreground': ThemeManager.COLORS['text']}
        
        # Thông tin cơ bản
        ttk.Label(form_frame, text="THÔNG TIN CƠ BẢN",
                 **heading_style).pack(anchor='w', pady=(0, 15))
        
        info_frame = ttk.Frame(form_frame)
        info_frame.pack(fill='x', pady=(0, 30))
        
        # Username
        field_frame = ttk.Frame(info_frame)
        field_frame.pack(fill='x', pady=5)
        ttk.Label(field_frame, text="👤 Tên đăng nhập:", **label_style).pack(side='left')
        ttk.Label(field_frame, text=user.get('username', ''), **value_style).pack(side='left', padx=(10, 0))
        
        # Email
        field_frame = ttk.Frame(info_frame)
        field_frame.pack(fill='x', pady=5)
        ttk.Label(field_frame, text="✉️ Email:", **label_style).pack(side='left')
        ttk.Label(field_frame, text=user.get('email', ''), **value_style).pack(side='left', padx=(10, 0))
        
        # Ngày tham gia
        join_date = datetime.fromisoformat(user.get('join_date', datetime.now().isoformat()))
        field_frame = ttk.Frame(info_frame)
        field_frame.pack(fill='x', pady=5)
        ttk.Label(field_frame, text="📅 Ngày tham gia:", **label_style).pack(side='left')
        ttk.Label(field_frame, text=join_date.strftime('%d/%m/%Y'), **value_style).pack(side='left', padx=(10, 0))
        
        # Đường kẻ phân cách
        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Thống kê
        ttk.Label(form_frame, text="THỐNG KÊ HOẠT ĐỘNG",
                 **heading_style).pack(anchor='w', pady=(0, 15))
        
        stats_frame = ttk.Frame(form_frame)
        stats_frame.pack(fill='x')
        
        # Số manga yêu thích
        favorites_count = len(user.get('favorites', []))
        field_frame = ttk.Frame(stats_frame)
        field_frame.pack(fill='x', pady=5)
        ttk.Label(field_frame, text="❤️ Manga yêu thích:", **label_style).pack(side='left')
        ttk.Label(field_frame, text=str(favorites_count), **value_style).pack(side='left', padx=(10, 0))
        
        # Quyền hạn
        field_frame = ttk.Frame(stats_frame)
        field_frame.pack(fill='x', pady=5)
        ttk.Label(field_frame, text="👑 Quyền hạn:", **label_style).pack(side='left')
        role_text = "Quản trị viên" if user.get('is_admin', False) else "Thành viên"
        role_label = ttk.Label(field_frame, text=role_text,
                             font=ThemeManager.FONTS['body_bold'],
                             foreground=ThemeManager.COLORS['primary'])
        role_label.pack(side='left', padx=(10, 0))
        
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
