import os
import sys

from src.main import main

SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, SRC_PATH)

if __name__ == "__main__":
    main()
