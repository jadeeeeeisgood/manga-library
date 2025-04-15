import tkinter as tk
from tkinter import ttk

class ThemeManager:
    # Màu sắc
    COLORS = {
        'primary': '#3498DB',  # Xanh dương đậm
        'primary_dark': '#2980B9',  # Xanh dương tối
        'secondary': '#2ECC71',  # Xanh lá
        'secondary_dark': '#27AE60',  # Xanh lá tối
        'background': '#ECF0F1',  # Xám nhạt
        'surface': '#FFFFFF',  # Trắng
        'text': '#2C3E50',  # Xanh đen
        'text_secondary': '#7F8C8D',  # Xám
        'error': '#E74C3C',  # Đỏ
        'warning': '#F1C40F',  # Vàng
        'success': '#2ECC71',  # Xanh lá
    }

    # Font chữ
    FONTS = {
        'heading': ('Helvetica', 20, 'bold'),
        'subheading': ('Helvetica', 16, 'bold'),
        'body': ('Helvetica', 11),
        'body_bold': ('Helvetica', 11, 'bold'),
        'small': ('Helvetica', 9),
    }

    # Style cho buttons
    BUTTON_STYLES = {
        'primary': {
            'font': FONTS['body_bold'],
            'bg': COLORS['primary'],
            'fg': 'white',
            'bd': 0,
            'width': 20,
            'height': 2,
            'cursor': 'hand2'
        },
        'secondary': {
            'font': FONTS['body'],
            'bg': COLORS['background'],
            'fg': COLORS['text'],
            'bd': 0,
            'width': 20,
            'height': 2,
            'cursor': 'hand2'
        },
        'danger': {
            'font': FONTS['body_bold'],
            'bg': COLORS['error'],
            'fg': 'white',
            'bd': 0,
            'width': 20,
            'height': 2,
            'cursor': 'hand2'
        }
    }

    @staticmethod
    def setup_theme():
        """Thiết lập theme cho toàn bộ ứng dụng"""
        style = ttk.Style()
        
        # Sử dụng theme clam làm base
        style.theme_use('clam')
        
        # Configure style cho ttk widgets
        style.configure('TLabel', 
                      font=ThemeManager.FONTS['body'],
                      foreground=ThemeManager.COLORS['text'])
        
        style.configure('Heading.TLabel',
                      font=ThemeManager.FONTS['heading'],
                      foreground=ThemeManager.COLORS['text'])
        
        style.configure('Subheading.TLabel',
                      font=ThemeManager.FONTS['subheading'],
                      foreground=ThemeManager.COLORS['text'])
        
        style.configure('TEntry',
                      font=ThemeManager.FONTS['body'],
                      fieldbackground=ThemeManager.COLORS['surface'])
        
        style.configure('TButton',
                      font=ThemeManager.FONTS['body_bold'],
                      background=ThemeManager.COLORS['primary'])
        
        style.configure('Secondary.TButton',
                      background=ThemeManager.COLORS['background'])
        
        style.configure('Danger.TButton',
                      background=ThemeManager.COLORS['error'])
        
        style.configure('TFrame',
                      background=ThemeManager.COLORS['surface'])
        
        style.configure('Card.TFrame',
                      background=ThemeManager.COLORS['surface'],
                      relief='raised',
                      borderwidth=1)
        
        # Configure style cho Treeview
        style.configure('Treeview',
                      font=ThemeManager.FONTS['body'],
                      rowheight=30,
                      background=ThemeManager.COLORS['surface'],
                      foreground=ThemeManager.COLORS['text'],
                      fieldbackground=ThemeManager.COLORS['surface'])
        
        style.configure('Treeview.Heading',
                      font=ThemeManager.FONTS['body_bold'],
                      background=ThemeManager.COLORS['background'])
        
        # Hiệu ứng hover cho Treeview
        style.map('Treeview',
                 background=[('selected', ThemeManager.COLORS['primary'])],
                 foreground=[('selected', 'white')])

    @staticmethod
    def create_gradient_background(canvas, width, height, start_color='#E8F0FE', end_color='#FFFFFF'):
        """Tạo background gradient"""
        for i in range(height):
            # Tính toán màu gradient
            ratio = i / height
            r1, g1, b1 = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
            r2, g2, b2 = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)

    @staticmethod
    def apply_button_hover_effect(button, style='primary'):
        """Thêm hiệu ứng hover cho button"""
        if isinstance(button, tk.Button):
            original_color = ThemeManager.BUTTON_STYLES[style]['bg']
            hover_color = ThemeManager.COLORS['primary_dark'] if style == 'primary' else \
                         ThemeManager.COLORS['secondary_dark'] if style == 'secondary' else \
                         '#C0392B'  # darker red for danger
            
            button.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
            button.bind('<Leave>', lambda e: e.widget.config(bg=original_color))

    @staticmethod
    def create_rounded_button(parent, text, command, style='primary', width=20, height=2):
        """Tạo button với góc bo tròn và style định sẵn"""
        button = tk.Button(parent, text=text, command=command,
                         **ThemeManager.BUTTON_STYLES[style])
        ThemeManager.apply_button_hover_effect(button, style)
        return button