from app import create_app

app = create_app()

@app.route('/')
def index():
    return "<h1>Index page of python full stack project</h1>"


if __name__ == '__main__':
    app.run()