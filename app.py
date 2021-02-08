from flask import Flask
import global_var
from flask_cors import CORS
import config
from apis.management import management
from dao.management import Management

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
global_var.db.init_app(app)
CORS(app)

with app.app_context():
    global_var.db.drop_all()
    global_var.db.create_all()
    m = Management(username='admin', password='21232f297a57a5a743894a0e4a801fc3')
    global_var.db.session.add(m)
    global_var.db.session.commit()

app.register_blueprint(management)
if __name__ == '__main__':
    app.run()
