import socket

import requests
from logger import logger

req_session = requests.session()

def get_host_ip():
    """
    查询本机内网ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_public_net_ip():
    """获得外网IP，与百度搜索结果相同"""
    res1 = req_session.get('http://ip.cip.cc/')
    return res1.text.strip()

def get_timezone_geolocation_gaode(ip):
    # 高德IP查询接口
    # https://lbs.amap.com/api/webservice/guide/api/ipconfig
    for i in range(3):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            }
            url = 'https://restapi.amap.com/v5/ip?parameters'
            params = {
                'key': 'your key',
                'type': 4,
                'ip': ip,
            }
            r = req_session.get(url, headers=headers, params=params)
            data = r.json()
            location = data.get('location')
            lon, lat = location.split(',')
            return {'lon': float(lon), 'lat': float(lat)}
        except Exception as e:
            logger.error(f'get ip failed, error: {e}', exc_info=True)
    return None


def get_timezone_geolocation_ipapi(ip):
    for i in range(3):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            }
            url = f"http://ip-api.com/json/{ip}"
            response = req_session.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f'get ip failed, error: {e}', exc_info=True)
    return None

def get_timezone_geolocation(ip):
    """get geo location"""
    data = get_timezone_geolocation_ipapi(ip)
    if not data:
        data = get_timezone_geolocation_gaode(ip)
        if not data:
            return {}
        return data
    return data



