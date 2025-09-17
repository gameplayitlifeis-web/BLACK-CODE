from app import app  # Make sure app.py exists in the backend folder

if __name__ == "__main__":
    print("Starting backend server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
