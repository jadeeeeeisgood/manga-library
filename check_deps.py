import importlib
import sys

required_packages = [
    'Pillow',
    'requests',
    'python-dateutil'
]

def check_dependencies():
    missing_packages = []
    
    print("Checking dependencies...")
    for package in required_packages:
        try:
            importlib.import_module(package.lower())
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print("\nMissing packages detected. Install using:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    else:
        print("\nAll dependencies are satisfied!")

if __name__ == "__main__":
    check_dependencies()
