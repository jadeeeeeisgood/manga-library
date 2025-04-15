import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.status_utils import StatusMapping
from ..utils.theme_utils import ThemeManager

class SearchAPIDialog(tk.Toplevel):
    def __init__(self, parent, manga_manager):
        super().__init__(parent)
        self.manga_manager = manga_manager
        
        self.title("Tìm kiếm manga từ MyAnimeList")
        # Tăng kích thước cửa sổ và cho phép resize
        self.geometry("1000x800")
        self.resizable(True, True)
        
        # Tạo gradient background
        self.create_gradient_background()
        
        # Tạo main frame với scrollbar
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas và scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the widgets
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_widgets(self.scrollable_frame)
        self.search_results = []
        
        # Làm cho dialog trở thành modal
        self.transient(parent)
        self.grab_set()

    def create_gradient_background(self):
        self.bg_canvas = tk.Canvas(self, width=1000, height=800)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        ThemeManager.create_gradient_background(self.bg_canvas, 1000, 800)

    def create_widgets(self, parent):
        # Header với padding lớn hơn
        header_frame = ttk.Frame(parent, padding="30")
        header_frame.pack(fill='x')
        
        # Logo và tiêu đề
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='center', pady=(0, 30))
        
        logo_label = ttk.Label(title_frame, text="🔍", font=('Helvetica', 32))
        logo_label.pack(pady=(0, 15))
        
        title_label = ttk.Label(title_frame, 
                              text="Tìm kiếm trên MyAnimeList",
                              style='Heading.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                text="Nhập tên manga bạn muốn tìm",
                                font=ThemeManager.FONTS['body'],
                                foreground=ThemeManager.COLORS['text_secondary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Khung tìm kiếm với padding lớn hơn
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(fill='x', pady=(20, 30))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, 
                               textvariable=self.search_var,
                               font=ThemeManager.FONTS['body'],
                               width=50)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<Return>', lambda e: self.search_manga())
        
        search_btn = ThemeManager.create_rounded_button(
            search_frame,
            text="🔍 Tìm kiếm",
            command=self.search_manga,
            style='primary',
            width=15
        )
        search_btn.pack(side=tk.LEFT)
        
        # Đường kẻ phân cách
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=30)
        
        # Kết quả tìm kiếm với padding lớn hơn
        result_frame = ttk.Frame(parent, padding="30")
        result_frame.pack(fill='both', expand=True)
        
        # Treeview với style mới và kích thước lớn hơn
        columns = ('title', 'author', 'status', 'rating', 'members')
        self.result_tree = ttk.Treeview(result_frame, 
                                      columns=columns,
                                      show='headings',
                                      height=15,
                                      style='Treeview')
        
        # Định nghĩa các cột với kích thước phù hợp hơn
        headings = {
            'title': ('Tiêu đề', 400),
            'author': ('Tác giả', 200),
            'status': ('Trạng thái', 150),
            'rating': ('Điểm', 100),
            'members': ('Lượt đọc', 100)
        }
        
        for col, (text, width) in headings.items():
            self.result_tree.heading(col, text=text)
            self.result_tree.column(col, width=width)
        
        # Scrollbar với style
        scrollbar = ttk.Scrollbar(result_frame,
                                orient=tk.VERTICAL,
                                command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout với trọng số
        self.result_tree.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        
        # Footer frame với padding lớn hơn
        footer_frame = ttk.Frame(parent, padding="30")
        footer_frame.pack(fill='x')
        
        # Nút điều khiển
        btn_frame = ttk.Frame(footer_frame)
        btn_frame.pack(anchor='center', pady=(20, 0))
        
        add_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="➕ Thêm vào thư viện",
            command=self.add_selected,
            style='primary'
        )
        add_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = ThemeManager.create_rounded_button(
            btn_frame,
            text="Đóng",
            command=self.destroy,
            style='secondary'
        )
        close_btn.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = ttk.Label(footer_frame,
                                    text="",
                                    font=ThemeManager.FONTS['small'],
                                    foreground=ThemeManager.COLORS['text_secondary'])
        self.status_label.pack(pady=(20, 0))
        
        # Bind double click
        self.result_tree.bind('<Double-1>', lambda e: self.add_selected())

    def search_manga(self):
        """Tìm kiếm manga từ API"""
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        # Xóa kết quả cũ
        self.result_tree.delete(*self.result_tree.get_children())
        self.status_label.config(text="Đang tìm kiếm...")
        self.update()
        
        # Tìm kiếm
        self.search_results = self.manga_manager.fetch_manga_from_jikan(keyword)
        
        if not self.search_results:
            self.status_label.config(text="Không tìm thấy kết quả nào.")
            return
        
        # Hiển thị kết quả
        for i, manga in enumerate(self.search_results):
            self.result_tree.insert('', 'end', values=(
                manga.get('title', ''),
                manga.get('author', ''),
                StatusMapping.to_vietnamese(manga.get('status', '')),
                manga.get('rating', ''),
                f"{manga.get('members', 0):,}"
            ), tags=(str(i),))
        
        self.status_label.config(text=f"Tìm thấy {len(self.search_results)} kết quả.")

    def add_selected(self):
        """Thêm manga được chọn vào thư viện"""
        selection = self.result_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một manga để thêm vào thư viện!")
            return
        
        # Lấy manga được chọn
        item = self.result_tree.item(selection[0])
        index = int(item['tags'][0])
        manga = self.search_results[index]
        
        # Thêm vào collection
        manga_id = self.manga_manager.add_manga(manga)
        
        if manga_id:
            messagebox.showinfo("Thành công", f"Đã thêm '{manga['title']}' vào thư viện!")
            # Xóa item đã thêm khỏi danh sách
            self.result_tree.delete(selection)
            self.search_results.pop(index)
        else:
            messagebox.showerror("Lỗi", "Không thể thêm manga vào thư viện. Vui lòng thử lại!")
