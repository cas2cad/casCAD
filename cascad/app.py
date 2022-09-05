from cascad.server import create_app
from cascad.settings import BASE_DIR


app = create_app()
app.run("127.0.0.1", 5000)