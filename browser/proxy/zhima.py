import time

import requests



class ZhiMa:
    """https://www.zhimaruanjian.com/"""

    def __init__(self):
        self.app_key = ''
        self.session = requests.session()

    def get_proxy(self, num, pro=0, city=0):
        """
        :param num
        :param pro
        :param city
        :return
        """
        # 直连IP
        url = f'http://webapi.http.zhimacangku.com/getip?num={num}&type=2&pro={pro}&city=0&yys=0&port=1&time=2&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions='
        proxy_info = None
        for i in range(5):
            r = self.session.get(url)
            proxy_info = r.json()
            code = proxy_info.get('code', 0)
            if code == 113:
                ip = proxy_info.get('msg').replace('', '')
                self.add_whitelist(ip)
            elif code == 111:
                # 请2秒后再试
                sleep_time = proxy_info.get('msg')[1]
                time.sleep(int(sleep_time))
            elif code == 0:
                break
        if not proxy_info:
            raise
        proxy_data = proxy_info.get('data')
        proxy_data = proxy_data[0]
        proxy = proxy_data['ip'] + ':' + str(proxy_data['port'])
        return proxy

    def add_whitelist(self, ip):
        """
        :param ip
        :return
        """
        url = f'https://wapi.http.linkudp.com/index/index/save_white?neek=326117&appkey={self.app_key}&white={ip}'
        r = requests.get(url)
        return r.json()
