from models import db
from models.user import User
from models.attack_log import AttackLog

def init_db():
    db.create_all()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_db()
        print("Database initialized successfully.")
