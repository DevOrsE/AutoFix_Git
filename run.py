# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="10.8.1.20", port=5000, debug=True)