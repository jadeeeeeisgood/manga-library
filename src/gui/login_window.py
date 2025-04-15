import tkinter as tk
from tkinter import ttk, messagebox
import re

class LoginWindow(tk.Toplevel):
    def __init__(self, parent, auth_manager, on_login_success):
        print("Initializing LoginWindow...")
        super().__init__(parent)
        self.title("Đăng nhập")
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        
        # Cấu hình cửa sổ
        window_width = 400
        window_height = 450  # Tăng chiều cao
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        
        # Tạo gradient background
        self.create_gradient_background()
        
        self.create_widgets()
        print("LoginWindow widgets created")
        
        # Không cho phép tương tác với cửa sổ chính khi đang đăng nhập
        self.transient(parent)
        self.grab_set()
        print("LoginWindow initialized")

    def create_gradient_background(self):
        # Tạo canvas cho gradient background
        self.bg_canvas = tk.Canvas(self, width=400, height=450)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Vẽ gradient
        for i in range(450):
            color = self.gradient_color('#E8F0FE', '#FFFFFF', i/450)
            self.bg_canvas.create_line(0, i, 400, i, fill=color)

    def gradient_color(self, start_color, end_color, ratio):
        # Chuyển đổi màu hex thành RGB
        start_rgb = [int(start_color[i:i+2], 16) for i in (1, 3, 5)]
        end_rgb = [int(end_color[i:i+2], 16) for i in (1, 3, 5)]
        
        # Tính toán màu gradient
        current_rgb = [int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio) for i in range(3)]
        return '#{:02x}{:02x}{:02x}'.format(*current_rgb)

    def create_widgets(self):
        # Frame chính với background trong suốt
        main_frame = ttk.Frame(self, style='Transparent.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo placeholder (có thể thay bằng ảnh thật)
        logo_frame = ttk.Frame(main_frame, width=100, height=100)
        logo_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        logo_label = ttk.Label(logo_frame, text="📚", font=('Helvetica', 48))
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Tiêu đề với style mới
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        title_label = ttk.Label(title_frame, text="ĐĂNG NHẬP", 
                              font=('Helvetica', 20, 'bold'),
                              foreground='#2C3E50')
        title_label.pack()
        
        # Style cho entry fields
        entry_style = {'font': ('Helvetica', 11), 'width': 25}
        
        # Username với icon
        username_frame = ttk.Frame(main_frame)
        username_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(username_frame, text="👤", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var, **entry_style)
        self.username_entry.pack(side=tk.LEFT)
        self.username_entry.insert(0, "Tên đăng nhập")
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Tên đăng nhập"))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Tên đăng nhập"))
        
        # Password với icon và toggle
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=3, column=0, columnspan=2, pady=(0, 25))
        ttk.Label(password_frame, text="🔒", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", **entry_style)
        self.password_entry.pack(side=tk.LEFT)
        self.password_entry.insert(0, "Mật khẩu")
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Mật khẩu"))
        self.password_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Mật khẩu"))
        
        # Toggle password visibility button
        self.show_password = False
        self.toggle_btn = ttk.Label(password_frame, text="👁️", font=('Helvetica', 12), cursor="hand2")
        self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        self.toggle_btn.bind('<Button-1>', self.toggle_password_visibility)
        
        # Nút Đăng nhập với style mới
        login_button = tk.Button(main_frame, text="Đăng nhập",
                               font=('Helvetica', 11, 'bold'),
                               bg='#3498DB', fg='white',
                               width=20, height=2,
                               bd=0, cursor='hand2')
        login_button.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        login_button.bind('<Enter>', lambda e: e.widget.config(bg='#2980B9'))
        login_button.bind('<Leave>', lambda e: e.widget.config(bg='#3498DB'))
        login_button.config(command=self.login)
        
        # Đường kẻ phân cách
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        # Nút chuyển sang đăng ký với style mới
        register_button = tk.Button(main_frame, text="Tạo tài khoản mới",
                                  font=('Helvetica', 11),
                                  bg='#ECF0F1', fg='#2C3E50',
                                  width=20, height=2,
                                  bd=0, cursor='hand2')
        register_button.grid(row=6, column=0, columnspan=2)
        register_button.bind('<Enter>', lambda e: e.widget.config(bg='#BDC3C7'))
        register_button.bind('<Leave>', lambda e: e.widget.config(bg='#ECF0F1'))
        register_button.config(command=self.show_register)
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.login())

    def on_entry_click(self, event, placeholder):
        """Xử lý khi click vào entry field"""
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            if placeholder == "Mật khẩu":
                widget.config(show="*")

    def on_focus_out(self, event, placeholder):
        """Xử lý khi focus ra khỏi entry field"""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, placeholder)
            if placeholder == "Mật khẩu":
                widget.config(show="")

    def toggle_password_visibility(self, event):
        """Toggle the visibility of the password"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="🔒")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="👁️")

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        success, message = self.auth_manager.login(username, password)
        if success:
            messagebox.showinfo("Thành công", message)
            self.on_login_success()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message)

    def show(self):
        """Hiển thị lại cửa sổ đăng nhập"""
        self.deiconify()  # Hiện lại cửa sổ đã ẩn
    
    def show_register(self):
        """Show the registration window"""
        self.withdraw()  # Hide login window
        register_window = RegisterWindow(self.master, self.auth_manager, lambda: self.deiconify())
        register_window.protocol("WM_DELETE_WINDOW", lambda: self.on_register_close(register_window))

    def on_register_close(self, register_window):
        register_window.destroy()
        self.show()  # Hiện lại cửa sổ đăng nhập

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent, auth_manager, on_close):
        super().__init__(parent)
        self.title("Đăng ký")
        self.auth_manager = auth_manager
        self.on_close = on_close
        
        # Cấu hình cửa sổ
        window_width = 400
        window_height = 550  # Tăng chiều cao
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        
        # Tạo gradient background
        self.create_gradient_background()
        
        self.create_widgets()
        
        # Không cho phép tương tác với cửa sổ chính
        self.transient(parent)
        self.grab_set()

    def create_gradient_background(self):
        # Tạo canvas cho gradient background
        self.bg_canvas = tk.Canvas(self, width=400, height=550)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Vẽ gradient
        for i in range(550):
            color = self.gradient_color('#E8F0FE', '#FFFFFF', i/550)
            self.bg_canvas.create_line(0, i, 400, i, fill=color)

    def gradient_color(self, start_color, end_color, ratio):
        # Chuyển đổi màu hex thành RGB
        start_rgb = [int(start_color[i:i+2], 16) for i in (1, 3, 5)]
        end_rgb = [int(end_color[i:i+2], 16) for i in (1, 3, 5)]
        
        # Tính toán màu gradient
        current_rgb = [int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio) for i in range(3)]
        return '#{:02x}{:02x}{:02x}'.format(*current_rgb)

    def create_widgets(self):
        # Frame chính với background trong suốt
        main_frame = ttk.Frame(self, style='Transparent.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo placeholder
        logo_frame = ttk.Frame(main_frame, width=100, height=100)
        logo_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        logo_label = ttk.Label(logo_frame, text="📝", font=('Helvetica', 48))
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Tiêu đề với style mới
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        title_label = ttk.Label(title_frame, text="ĐĂNG KÝ TÀI KHOẢN", 
                              font=('Helvetica', 20, 'bold'),
                              foreground='#2C3E50')
        title_label.pack()
        
        # Style cho entry fields
        entry_style = {'font': ('Helvetica', 11), 'width': 25}
        
        # Username với icon
        username_frame = ttk.Frame(main_frame)
        username_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(username_frame, text="👤", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var, **entry_style)
        self.username_entry.pack(side=tk.LEFT)
        self.username_entry.insert(0, "Tên đăng nhập")
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Tên đăng nhập"))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Tên đăng nhập"))
        
        # Email với icon
        email_frame = ttk.Frame(main_frame)
        email_frame.grid(row=3, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(email_frame, text="✉️", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(email_frame, textvariable=self.email_var, **entry_style)
        self.email_entry.pack(side=tk.LEFT)
        self.email_entry.insert(0, "Email")
        self.email_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Email"))
        self.email_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Email"))
        
        # Password với icon và toggle
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(password_frame, text="🔒", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", **entry_style)
        self.password_entry.pack(side=tk.LEFT)
        self.password_entry.insert(0, "Mật khẩu")
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Mật khẩu"))
        self.password_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Mật khẩu"))
        
        # Toggle password visibility button
        self.show_password = False
        self.toggle_btn = ttk.Label(password_frame, text="👁️", font=('Helvetica', 12), cursor="hand2")
        self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        self.toggle_btn.bind('<Button-1>', self.toggle_password_visibility)
        
        # Confirm Password với icon và toggle
        confirm_frame = ttk.Frame(main_frame)
        confirm_frame.grid(row=5, column=0, columnspan=2, pady=(0, 25))
        ttk.Label(confirm_frame, text="🔒", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(confirm_frame, textvariable=self.confirm_password_var, show="*", **entry_style)
        self.confirm_password_entry.pack(side=tk.LEFT)
        self.confirm_password_entry.insert(0, "Xác nhận mật khẩu")
        self.confirm_password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Xác nhận mật khẩu"))
        self.confirm_password_entry.bind('<FocusOut>', lambda e: self.on_focus_out(e, "Xác nhận mật khẩu"))
        
        # Toggle confirm password visibility button
        self.toggle_confirm_btn = ttk.Label(confirm_frame, text="👁️", font=('Helvetica', 12), cursor="hand2")
        self.toggle_confirm_btn.pack(side=tk.LEFT, padx=(5, 0))
        self.toggle_confirm_btn.bind('<Button-1>', self.toggle_confirm_password_visibility)
        
        # Nút Đăng ký với style mới
        register_button = tk.Button(main_frame, text="Đăng ký",
                                  font=('Helvetica', 11, 'bold'),
                                  bg='#2ECC71', fg='white',
                                  width=20, height=2,
                                  bd=0, cursor='hand2')
        register_button.grid(row=6, column=0, columnspan=2, pady=(0, 15))
        register_button.bind('<Enter>', lambda e: e.widget.config(bg='#27AE60'))
        register_button.bind('<Leave>', lambda e: e.widget.config(bg='#2ECC71'))
        register_button.config(command=self.register)
        
        # Đường kẻ phân cách
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        # Nút Quay lại với style mới
        back_button = tk.Button(main_frame, text="Quay lại đăng nhập",
                              font=('Helvetica', 11),
                              bg='#ECF0F1', fg='#2C3E50',
                              width=20, height=2,
                              bd=0, cursor='hand2')
        back_button.grid(row=8, column=0, columnspan=2)
        back_button.bind('<Enter>', lambda e: e.widget.config(bg='#BDC3C7'))
        back_button.bind('<Leave>', lambda e: e.widget.config(bg='#ECF0F1'))
        back_button.config(command=self.go_back)
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.register())

    def on_entry_click(self, event, placeholder):
        """Xử lý khi click vào entry field"""
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            if placeholder in ["Mật khẩu", "Xác nhận mật khẩu"]:
                widget.config(show="*")

    def on_focus_out(self, event, placeholder):
        """Xử lý khi focus ra khỏi entry field"""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, placeholder)
            if placeholder in ["Mật khẩu", "Xác nhận mật khẩu"]:
                widget.config(show="")

    def toggle_password_visibility(self, event):
        """Toggle the visibility of the password"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="🔒")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="👁️")

    def toggle_confirm_password_visibility(self, event):
        """Toggle the visibility of the confirm password field"""
        self.show_confirm_password = not getattr(self, 'show_confirm_password', False)
        if self.show_confirm_password:
            self.confirm_password_entry.config(show="")
            self.toggle_confirm_btn.config(text="🔒")
        else:
            self.confirm_password_entry.config(show="*")
            self.toggle_confirm_btn.config(text="👁️")

    def validate_email(self, email):
        """Kiểm tra định dạng email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Kiểm tra thông tin nhập
        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        success, message = self.auth_manager.register(username, password, email)
        if success:
            messagebox.showinfo("Thành công", message)
            self.go_back()
        else:
            messagebox.showerror("Lỗi", message)

    def go_back(self):
        """Return to login window"""
        self.destroy()
        if self.on_close:
            self.on_close()  # Show login window