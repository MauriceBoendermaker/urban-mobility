import os
import sys
import builtins

SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, SRC_PATH)

from src.utils.validation import safe_input

builtins.input = safe_input

from src.main import main

if __name__ == "__main__":
    main()
