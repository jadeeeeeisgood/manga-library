import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.theme_utils import ThemeManager

class ChangePasswordDialog(tk.Toplevel):
    def __init__(self, parent, auth_manager):
        super().__init__(parent)
        self.auth_manager = auth_manager
        
        self.title("Đổi mật khẩu")
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
        # Header
        header_frame = ttk.Frame(parent, padding="20")
        header_frame.pack(fill='x')
        
        # Logo và tiêu đề
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='center', pady=(0, 20))
        
        logo_label = ttk.Label(title_frame, text="🔐", font=('Helvetica', 32))
        logo_label.pack(pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                              text="Đổi Mật Khẩu",
                              style='Heading.TLabel')
        title_label.pack()
        
        # Form fields
        form_frame = ttk.Frame(parent, padding="20")
        form_frame.pack(fill='both', expand=True)
        
        # Style cho entry fields
        entry_style = {'width': 30, 'font': ThemeManager.FONTS['body']}
        label_style = {'font': ThemeManager.FONTS['body_bold'],
                      'foreground': ThemeManager.COLORS['text']}
        
        # Mật khẩu hiện tại
        ttk.Label(form_frame, text="🔑 Mật khẩu hiện tại:", **label_style).pack(
            anchor='w', pady=(0, 5))
        
        self.current_password_var = tk.StringVar()
        self.current_password_entry = ttk.Entry(form_frame, 
                                              textvariable=self.current_password_var,
                                              show="•",
                                              **entry_style)
        self.current_password_entry.pack(fill='x', pady=(0, 20))
        
        # Mật khẩu mới
        ttk.Label(form_frame, text="🔒 Mật khẩu mới:", **label_style).pack(
            anchor='w', pady=(0, 5))
        
        self.new_password_var = tk.StringVar()
        self.new_password_entry = ttk.Entry(form_frame,
                                          textvariable=self.new_password_var,
                                          show="•",
                                          **entry_style)
        self.new_password_entry.pack(fill='x', pady=(0, 20))
        
        # Xác nhận mật khẩu mới
        ttk.Label(form_frame, text="🔒 Xác nhận mật khẩu:", **label_style).pack(
            anchor='w', pady=(0, 5))
        
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(form_frame,
                                              textvariable=self.confirm_password_var,
                                              show="•",
                                              **entry_style)
        self.confirm_password_entry.pack(fill='x', pady=(0, 20))
        
        # Thông tin yêu cầu
        info_frame = ttk.Frame(form_frame)
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_icon = ttk.Label(info_frame, text="ℹ️", font=('Helvetica', 16))
        info_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        info_text = ("Mật khẩu phải có:\n"
                    "• Ít nhất 6 ký tự\n"
                    "• Bao gồm chữ và số")
        
        info_label = ttk.Label(info_frame,
                             text=info_text,
                             font=ThemeManager.FONTS['small'],
                             foreground=ThemeManager.COLORS['text_secondary'],
                             justify=tk.LEFT)
        info_label.pack(side=tk.LEFT)
        
        # Nút điều khiển
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20)
        
        change_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="✓ Đổi mật khẩu",
            command=self.change_password,
            style='primary'
        )
        change_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="Hủy",
            command=self.destroy,
            style='secondary'
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.change_password())

    def validate_password(self, password):
        """Kiểm tra mật khẩu hợp lệ"""
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
        
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        
        if not (has_letter and has_number):
            return False, "Mật khẩu phải bao gồm cả chữ và số"
        
        return True, ""

    def change_password(self):
        """Xử lý đổi mật khẩu"""
        current_password = self.current_password_var.get()
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Kiểm tra mật khẩu hiện tại
        if not current_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu hiện tại!")
            return
        
        # Kiểm tra mật khẩu mới
        if not new_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu mới!")
            return
        
        # Kiểm tra xác nhận mật khẩu
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        # Kiểm tra độ mạnh của mật khẩu mới
        is_valid, message = self.validate_password(new_password)
        if not is_valid:
            messagebox.showerror("Lỗi", message)
            return
        
        # Thực hiện đổi mật khẩu
        success, message = self.auth_manager.change_password(current_password, new_password)
        
        if success:
            messagebox.showinfo("Thành công", message)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message)
