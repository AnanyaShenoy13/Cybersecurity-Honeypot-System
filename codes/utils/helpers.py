import requests
from config import Config

def get_ip_geolocation(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data['country'],
                'regionName': data['regionName'],
                'city': data['city'],
                'lat': data['lat'],
                'lon': data['lon'],
                'isp': data['isp']
            }
        else:
            return None
    except Exception as e:
        print(f'Error fetching geolocation data: {str(e)}')
        return None

def log_attack(attack_type, ip_address, details):
    from models import db
    from models.attack_log import AttackLog
    from datetime import datetime

    attack_log = AttackLog(timestamp=datetime.now(), ip_address=ip_address, attack_type=attack_type, details=details)
    db.session.add(attack_log)
    db.session.commit()
