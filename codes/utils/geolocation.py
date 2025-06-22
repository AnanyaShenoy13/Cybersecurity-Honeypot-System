import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

def get_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data['country'],
                'region': data['regionName'],
                'city': data['city'],
                'zip': data['zip'],
                'lat': data['lat'],
                'lon': data['lon'],
                'timezone': data['timezone'],
                'isp': data['isp'],
                'org': data['org'],
                'as': data['as']
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching geolocation data: {e}")
        return None
