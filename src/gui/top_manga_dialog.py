import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.status_utils import StatusMapping
from ..utils.theme_utils import ThemeManager

class TopMangaDialog(tk.Toplevel):
    def __init__(self, parent, manga_manager):
        super().__init__(parent)
        self.manga_manager = manga_manager
        
        self.title("Top Manga - MyAnimeList")
        # Tăng kích thước cửa sổ
        self.geometry("1000x800")
        self.resizable(True, True)  # Cho phép thay đổi kích thước
        
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
        self.top_manga_results = []
        self.load_top_manga()
        
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
        
        logo_label = ttk.Label(title_frame, text="🏆", font=('Helvetica', 32))
        logo_label.pack(pady=(0, 15))
        
        title_label = ttk.Label(title_frame, 
                              text="Top Manga - MyAnimeList",
                              style='Heading.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                text="Những manga được đánh giá cao nhất",
                                font=ThemeManager.FONTS['body'],
                                foreground=ThemeManager.COLORS['text_secondary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Đường kẻ phân cách
        ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=30)
        
        # Danh sách manga với padding lớn hơn
        list_frame = ttk.Frame(parent, padding="30")
        list_frame.pack(fill='both', expand=True)
        
        # Treeview với style mới và kích thước lớn hơn
        columns = ('rank', 'title', 'status', 'rating', 'members')
        self.manga_tree = ttk.Treeview(list_frame, 
                                     columns=columns,
                                     show='headings',
                                     height=15,
                                     style='Treeview')
        
        # Định nghĩa các cột với kích thước phù hợp hơn
        headings = {
            'rank': ('Xếp hạng', 100),
            'title': ('Tiêu đề', 400),
            'status': ('Trạng thái', 150),
            'rating': ('Điểm', 100),
            'members': ('Lượt đọc', 150)
        }
        
        for col, (text, width) in headings.items():
            self.manga_tree.heading(col, text=text)
            self.manga_tree.column(col, width=width)
        
        # Scrollbar với style
        scrollbar = ttk.Scrollbar(list_frame,
                                orient=tk.VERTICAL,
                                command=self.manga_tree.yview)
        self.manga_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout với trọng số
        self.manga_tree.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
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
        self.manga_tree.bind('<Double-1>', lambda e: self.add_selected())

    def load_top_manga(self):
        """Tải danh sách top manga từ API"""
        # Hiển thị thông báo loading
        self.manga_tree.insert('', 'end', values=('Loading...', '', '', '', ''))
        self.update()
        
        # Lấy danh sách top manga
        self.top_manga_results = self.manga_manager.fetch_top_manga(limit=20)
        
        # Xóa thông báo loading
        self.manga_tree.delete(*self.manga_tree.get_children())
        
        if not self.top_manga_results:
            self.status_label.config(text="Không thể tải danh sách top manga. Vui lòng thử lại sau!")
            return
        
        # Hiển thị kết quả
        for manga in self.top_manga_results:
            self.manga_tree.insert('', 'end', values=(
                manga.get('rank', 'N/A'),
                manga.get('title', ''),
                StatusMapping.to_vietnamese(manga.get('status', '')),
                manga.get('rating', ''),
                f"{manga.get('members', 0):,}"
            ), tags=(str(self.top_manga_results.index(manga)),))
        
        self.status_label.config(text=f"Đã tải {len(self.top_manga_results)} manga.")

    def add_selected(self):
        """Thêm manga được chọn vào thư viện"""
        selection = self.manga_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một manga để thêm vào thư viện!")
            return
        
        # Lấy manga được chọn
        item = self.manga_tree.item(selection[0])
        index = int(item['tags'][0])
        manga = self.top_manga_results[index]
        
        # Thêm vào collection
        manga_id = self.manga_manager.add_manga(manga)
        
        if manga_id:
            messagebox.showinfo("Thành công", f"Đã thêm '{manga['title']}' vào thư viện!")
            # Xóa item đã thêm khỏi danh sách
            self.manga_tree.delete(selection)
            self.top_manga_results.pop(index)
        else:
            messagebox.showerror("Lỗi", "Không thể thêm manga vào thư viện. Vui lòng thử lại!")
