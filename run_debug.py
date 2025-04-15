import sys
import traceback
from main import main

if __name__ == "__main__":
    try:
        print("Starting application in debug mode...")
        print(f"Python version: {sys.version}")
        print(f"Python path: {sys.path}")
        print("="*50)
        main()
    except Exception as e:
        print("\nError occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        print("="*50)
        sys.exit(1)
