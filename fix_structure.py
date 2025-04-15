import os
import shutil

def fix_structure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define required directories
    required_dirs = [
        os.path.join(base_dir, "assets", "cache"),
        os.path.join(base_dir, "data")
    ]
    
    print("Current structure:")
    for root, dirs, files in os.walk(base_dir):
        print(f"\nDirectory: {root}")
        print("Files:", files)
    
    # Create required directories
    print("\nCreating required directories...")
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created: {dir_path}")
    
    # Check for nested manga_library directory
    nested_dir = os.path.join(base_dir, "manga_library")
    if os.path.exists(nested_dir):
        print(f"\nFound nested directory at {nested_dir}")
        print("Moving files and removing nested directory...")
        
        # Move nested files to correct locations
        if os.path.exists(os.path.join(nested_dir, "assets", "cache")):
            for item in os.listdir(os.path.join(nested_dir, "assets", "cache")):
                src = os.path.join(nested_dir, "assets", "cache", item)
                dst = os.path.join(base_dir, "assets", "cache", item)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"Moved: {item} to assets/cache")
        
        if os.path.exists(os.path.join(nested_dir, "data")):
            for item in os.listdir(os.path.join(nested_dir, "data")):
                src = os.path.join(nested_dir, "data", item)
                dst = os.path.join(base_dir, "data", item)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"Moved: {item} to data")
        
        # Remove nested directory
        try:
            shutil.rmtree(nested_dir)
            print("Removed nested directory successfully")
        except Exception as e:
            print(f"Error removing nested directory: {e}")
    
    print("\nFinal structure:")
    for root, dirs, files in os.walk(base_dir):
        print(f"\nDirectory: {root}")
        print("Files:", files)

if __name__ == "__main__":
    fix_structure()
