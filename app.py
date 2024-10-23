from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:flask_password@db/flask_db'
app.config['SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate for migrations
migrate = Migrate(app, db)

# Register blueprints after initializing db to avoid circular imports
def register_blueprints(app):
    from blueprints.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
