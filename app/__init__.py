from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Use Config class
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'app/static/Emp_photo'
    
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)
    
    with app.app_context():
        try:
            from . import models
            db.create_all()
            
            # Create default admin user if not exists
            from .models import User
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            raise e
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
