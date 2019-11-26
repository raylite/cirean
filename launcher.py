from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from cirean import create_app, db
from cirean.models import Publisher

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Publisher': Publisher}
