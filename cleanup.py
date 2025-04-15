import os
import shutil
from src.utils.path_utils import get_cache_dir, get_data_dir, get_project_root

def cleanup():
    print("Starting cleanup...")
    
    # Get correct paths
    project_root = get_project_root()
    cache_dir = get_cache_dir()
    data_dir = get_data_dir()
    
    # Old directory paths
    old_base = os.path.join(project_root, 'manga_library')
    old_cache = os.path.join(old_base, 'assets', 'cache')
    old_data = os.path.join(old_base, 'data')
    
    print(f"Moving files from:")
    print(f"Old cache: {old_cache}")
    print(f"Old data: {old_data}")
    print(f"To:")
    print(f"New cache: {cache_dir}")
    print(f"New data: {data_dir}")
    
    # Create new directories
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    # Move cache files
    if os.path.exists(old_cache):
        print("\nMoving cache files...")
        for file in os.listdir(old_cache):
            src = os.path.join(old_cache, file)
            dst = os.path.join(cache_dir, file)
            if os.path.isfile(src):
                if not os.path.exists(dst):
                    print(f"Moving {file}")
                    shutil.copy2(src, dst)
                else:
                    print(f"Skipping {file} (already exists)")
    
    # Move data files
    if os.path.exists(old_data):
        print("\nMoving data files...")
        for file in os.listdir(old_data):
            src = os.path.join(old_data, file)
            dst = os.path.join(data_dir, file)
            if os.path.isfile(src):
                if not os.path.exists(dst):
                    print(f"Moving {file}")
                    shutil.copy2(src, dst)
                else:
                    print(f"Skipping {file} (already exists)")
    
    # Remove old directory
    if os.path.exists(old_base):
        print("\nRemoving old directory...")
        try:
            shutil.rmtree(old_base)
            print("Old directory removed successfully")
        except Exception as e:
            print(f"Error removing old directory: {e}")
    
    print("\nCleanup completed!")

if __name__ == "__main__":
    cleanup()
