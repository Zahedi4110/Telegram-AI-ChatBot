# run.py

from src.main import app
import os

if __name__ == '__main__':
    # Ensure the app runs on the correct host and port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)