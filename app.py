from flask_migrate import Migrate

from botbase import create_app
from botbase.extensions import db

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
	app.run(
        debug=app.config['DEBUG'], 
        threaded=True, 
        host="0.0.0.0", 
        port=app.config['PORT'])