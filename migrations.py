from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from server import app
from fliprBack.models import *


manager = Manager(app)
migrate = Migrate(app, Base)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
