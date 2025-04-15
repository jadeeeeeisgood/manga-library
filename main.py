import sys
import os

print("="*50)
print("Starting application...")
print(f"Python version: {sys.version}")

# Add project root to Python path
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)
print(f"Base path: {base_path}")
print(f"Python path: {sys.path}")
print("="*50)

try:
    print("Importing required modules...")
    import tkinter as tk
    from tkinter import ttk
    from src.utils.path_utils import ensure_directories
    from src.auth.auth_manager import AuthManager
    from src.models.manga_manager import MangaManager
    from src.gui.main_window import MainWindow
    print("All modules imported successfully")
    print("="*50)

    def main():
        # Ensure required directories exist
        print("Creating required directories...")
        ensure_directories()
        print("Directories created")

        print("Creating root window...")
        root = tk.Tk()
        root.title("Thư viện Manga")
        
        # Configure main window
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        root.minsize(800, 600)
        print("Window configured")
        
        # Initialize managers
        print("Initializing managers...")
        auth_manager = AuthManager()
        manga_manager = MangaManager()
        print("Managers initialized")
        
        # Create main window
        print("Creating MainWindow instance...")
        main_window = MainWindow(root, auth_manager, manga_manager)
        print("MainWindow created")
        
        # Apply theme
        print("Applying theme...")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        print("Theme applied")
        print("="*50)
        
        print("Starting main event loop...")
        root.mainloop()
        print("Application closed")

    if __name__ == "__main__":
        main()

except Exception as e:
    print("="*50)
    print(f"ERROR: {str(e)}")
    print("-"*50)
    import traceback
    traceback.print_exc()
    print("="*50)
    sys.exit(1)
