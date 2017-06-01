import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from abcmain import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manage.command()
def create_dummy():
    """Run the linters."""
    sys.exit(subprocess.call(['flake8']))



if __name__ == '__main__':
    manager.run()
