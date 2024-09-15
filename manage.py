import eventlet
eventlet.monkey_patch()

from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app('config.ProdConfig')  # Adjust the config as needed
migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
