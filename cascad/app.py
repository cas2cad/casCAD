from cascad.server import create_app
from cascad.settings import BASE_DIR


app = create_app()
app.run("0.0.0.0", 5000)