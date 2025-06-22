from extensions import db

class AttackLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    attack_type = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)
