import requests



class KuaiDaiLi:
    """https://www.kuaidaili.com/"""

    def __init__(self, username, password, order_id, api_key):
        """
        :param username
        :param password
        :param api_key: API KEY
        """
        self.username = username
        self.password = password
        self.order_id = order_id
        self.api_key = api_key
        self.session = requests.session()

    def get_order_info(self):
        """
        https://www.kuaidaili.com/doc/api/getorderinfo/
        :return:
        """
        url = f'https://dev.kdlapi.com/api/getorderinfo?orderid={self.order_id}&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            raise
        return data.get('data', {})

    def get_tps_current_ip(self):
        """
        https://www.kuaidaili.com/doc/api/tpscurrentip/
        :return:
        """
        url = f'https://tps.kdlapi.com/api/tpscurrentip?orderid={self.order_id}&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            raise
        return data.get('data', {}).get('current_ip', '')

    def get_dps(self):
        """"""
        url = f'http://dps.kdlapi.com/api/getdps/?orderid={self.order_id}&num=1&pt=1&format=json&sep=1&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            raise
        proxy = data.get('data', {}).get('proxy_list')[0]
        return proxy
