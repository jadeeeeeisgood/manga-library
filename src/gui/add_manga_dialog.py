import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.status_utils import StatusMapping
from ..utils.theme_utils import ThemeManager

class AddMangaDialog(tk.Toplevel):
    def __init__(self, parent, manga_manager):
        super().__init__(parent)
        self.manga_manager = manga_manager
        
        self.title("Thêm manga mới")
        self.geometry("600x800")
        self.resizable(False, False)
        
        # Tạo gradient background cho toàn bộ cửa sổ
        self.bg_canvas = tk.Canvas(self, width=600, height=800)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        ThemeManager.create_gradient_background(self.bg_canvas, 600, 800)
        
        # Tạo main frame nằm ở giữa cửa sổ
        self.main_frame = ttk.Frame(self, style='Card.TFrame')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=550, height=750)
        
        self.create_widgets()
        
        # Modal dialog
        self.transient(parent)
        self.grab_set()

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.main_frame, padding="20")
        header_frame.pack(fill='x')
        
        # Logo và tiêu đề
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='center', pady=(0, 20))
        
        logo_label = ttk.Label(title_frame, text="➕", font=('Helvetica', 32))
        logo_label.pack(pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                              text="Thêm Manga Mới",
                              style='Heading.TLabel')
        title_label.pack()

        # Form scrollable frame
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        form_frame = ttk.Frame(canvas, padding="20")

        # Cấu hình scroll
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack các widget
        canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
        scrollbar.pack(side="right", fill="y", padx=(0,20))
        
        # Tạo window trong canvas
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        # Style cho entry fields
        entry_style = {'width': 40, 'font': ThemeManager.FONTS['body']}
        label_style = {'font': ThemeManager.FONTS['body_bold'],
                      'foreground': ThemeManager.COLORS['text']}
        
        # Các trường nhập liệu
        fields = [
            ("📚 Tiêu đề:", "title"),
            ("🈁 Tiêu đề tiếng Nhật:", "title_japanese"),
            ("👤 Tác giả:", "author"),
            ("📅 Năm xuất bản:", "year"),
            ("🏷️ Thể loại:", "genres", "Phân cách bằng dấu phẩy"),
            ("📖 Số tập:", "volumes"),
            ("📑 Số chương:", "chapters"),
            ("⭐ Xếp hạng:", "rating"),
            ("🖼️ Link ảnh:", "image_url", "Nhập URL ảnh bìa manga"),
        ]
        
        self.entries = {}
        
        # Tạo các field
        row_counter = 0  # Đếm số row thực tế
        for field_info in fields:
            label_text, field_name, *placeholder = field_info
            
            # Frame cho mỗi field để chứa label, entry và tooltip nếu có
            field_frame = ttk.Frame(form_frame)
            field_frame.grid(row=row_counter, column=0, sticky='ew', pady=(10, 5))
            row_counter += 1
            
            # Label
            label = ttk.Label(field_frame, text=label_text, **label_style)
            label.pack(side=tk.LEFT)
            
            # Info icon và tooltip cho trường link ảnh
            if field_name == "image_url":
                info_icon = ttk.Label(field_frame, text="ℹ️", font=('Helvetica', 12))
                info_icon.pack(side=tk.LEFT, padx=(5, 0))
                
                tooltip_text = ("URL của ảnh bìa manga.\n"
                              "Ví dụ: https://example.com/manga-cover.jpg\n"
                              "Định dạng hỗ trợ: JPG, PNG\n"
                              "Ảnh sẽ được tự động tải về và cache")
                
                self.create_tooltip(info_icon, tooltip_text)
            
            # Entry
            self.entries[field_name] = ttk.Entry(form_frame, **entry_style)
            self.entries[field_name].grid(row=row_counter, column=0, sticky='ew', pady=(0, 10))
            row_counter += 1
            
            # Placeholder text
            if placeholder:
                self.entries[field_name].insert(0, placeholder[0])
                self.entries[field_name].bind('<FocusIn>', 
                    lambda e, p=placeholder[0]: self.on_entry_click(e, p))
                self.entries[field_name].bind('<FocusOut>', 
                    lambda e, p=placeholder[0]: self.on_focus_out(e, p))
            
            # Thêm thông tin mô tả dưới trường link ảnh
            if field_name == "image_url":
                desc_text = ("💡 Chỉ cần paste link ảnh bìa manga từ một trang web. "
                           "Ảnh sẽ được tự động tải về và lưu trữ.")
                desc_label = ttk.Label(form_frame, 
                                     text=desc_text,
                                     font=ThemeManager.FONTS['small'],
                                     foreground=ThemeManager.COLORS['text_secondary'],
                                     wraplength=400)
                desc_label.grid(row=row_counter, column=0, sticky='w', pady=(0, 10))
                row_counter += 1
        
        # Trạng thái
        ttk.Label(form_frame, text="📊 Trạng thái:", **label_style).grid(
            row=row_counter, column=0, sticky='w', pady=(10, 5))
        row_counter += 1
        
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(form_frame, 
                                  textvariable=self.status_var,
                                  values=StatusMapping.get_vietnamese_statuses(),
                                  state='readonly',
                                  width=38,
                                  font=ThemeManager.FONTS['body'])
        status_combo.grid(row=row_counter, column=0, sticky='ew', pady=(0, 10))
        status_combo.current(0)
        row_counter += 1
        
        # Tóm tắt
        ttk.Label(form_frame, text="📝 Tóm tắt:", **label_style).grid(
            row=row_counter, column=0, sticky='w', pady=(10, 5))
        row_counter += 1
        
        self.synopsis_text = tk.Text(form_frame, 
                                   width=40, height=5,
                                   font=ThemeManager.FONTS['body'],
                                   wrap=tk.WORD)
        self.synopsis_text.grid(row=row_counter, column=0, sticky='ew', pady=(0, 20))
        row_counter += 1
        
        # Footer với nút điều khiển
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row_counter, column=0, pady=10)
        
        save_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="💾 Lưu",
            command=self.save_manga,
            style='primary'
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="Hủy",
            command=self.destroy,
            style='secondary'
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Cập nhật scroll region sau khi tất cả widgets được thêm vào
        form_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_entry_click(self, event, placeholder):
        """Xử lý khi click vào entry field"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def on_focus_out(self, event, placeholder):
        """Xử lý khi focus ra khỏi entry field"""
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)

    def save_manga(self):
        """Lưu thông tin manga mới"""
        # Thu thập dữ liệu từ các trường nhập liệu
        manga_data = {
            'title': self.entries['title'].get().strip(),
            'title_japanese': self.entries['title_japanese'].get().strip(),
            'author': self.entries['author'].get().strip(),
            'year': self.entries['year'].get().strip(),
            'genres': self.entries['genres'].get().strip(),
            'volumes': self.entries['volumes'].get().strip(),
            'chapters': self.entries['chapters'].get().strip(),
            'rating': self.entries['rating'].get().strip(),
            'image_url': self.entries['image_url'].get().strip(),
            'status': self.status_var.get(),
            'synopsis': self.synopsis_text.get('1.0', tk.END).strip()
        }
        
        # Kiểm tra các trường bắt buộc
        if not manga_data['title']:
            messagebox.showerror("Lỗi", "Vui lòng nhập tiêu đề manga!")
            return
            
        if not manga_data['author']:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên tác giả!")
            return
            
        if not manga_data['genres'] or manga_data['genres'] == "Phân cách bằng dấu phẩy":
            messagebox.showerror("Lỗi", "Vui lòng nhập thể loại!")
            return
            
        if not manga_data['status']:
            messagebox.showerror("Lỗi", "Vui lòng chọn trạng thái!")
            return
        
        # Thêm manga mới
        manga_id = self.manga_manager.add_manga(manga_data)
        
        if manga_id:
            messagebox.showinfo("Thành công", "Đã thêm manga mới!")
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm manga. Vui lòng thử lại!")

    def create_tooltip(self, widget, text):
        """Tạo tooltip khi hover chuột trên widget"""
        tooltip = None
        
        def enter(event):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # Tạo cửa sổ tooltip
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Tạo label trong tooltip
            label = ttk.Label(tooltip, text=text,
                            font=ThemeManager.FONTS['small'],
                            foreground=ThemeManager.COLORS['text'],
                            background=ThemeManager.COLORS['surface'],
                            wraplength=300,
                            padding=5)
            label.pack()
            
        def leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
