from flask import Flask
import global_var
from flask_cors import CORS
import config
from apis.management import management

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
global_var.db.init_app(app)
CORS(app)

with app.app_context():
    global_var.db.create_all()

app.register_blueprint(management)
if __name__ == '__main__':
    app.run()
