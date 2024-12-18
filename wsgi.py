from school_dashboard import server

# Export the server variable for gunicorn
app = server

if __name__ == "__main__":
    app.run() 