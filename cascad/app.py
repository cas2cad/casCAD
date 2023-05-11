import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from cascad.settings import BASE_DIR
from cascad.server import create_app

def main():
    app = create_app()
    app.run("0.0.0.0", 5000)
   
# svg
if __name__ == '__main__':
    main()
