# run.py
from app import create_app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True, host='127.0.0.1', port=5000)
