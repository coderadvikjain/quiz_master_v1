from flask import Flask, render_template
from models import *
from controllers import *
from qm_api import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_master.sqlite3"
app.config['SECRET_KEY'] = 'qwerty852'

db.init_app(app)

app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(qm_api)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/api-documentation')
def swagger_ui():
    return render_template('swagger_ui.html')

def create_admin():
    admin_user = User.query.filter_by(username="admin",role="admin").first()
    if not admin_user:
        new_admin = User(username="admin",password="iitm@1705",full_name='Admin',role='admin')
        db.session.add(new_admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)