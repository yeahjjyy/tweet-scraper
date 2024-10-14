from browser.proxy.kuaidaili import KuaiDaiLi
from browser.proxy.zhima import ZhiMa

KYAIDAILI = 1
ZHIMA = 2


class Proxy:
    def __init__(self, kuaidaili_params=None, zhima_params=None, proxy_type=KYAIDAILI):
        """

        :param kuaidaili_params:
        :param zhima_params:

        :param proxy_type:
        """
        if kuaidaili_params:
            self.kuaidaili = KuaiDaiLi(**kuaidaili_params)
        if zhima_params:
            self.zhima = ZhiMa(**zhima_params)
        self.proxy_type = proxy_type

    def get_proxy_requests(self):
        if self.proxy_type == KYAIDAILI:
            proxy = self.kuaidaili.get_dps()
            proxies = {
                "http": f"http://{self.kuaidaili.username}:{self.kuaidaili.password}@{proxy}/",
                "https": f"http://{self.kuaidaili.username}:{self.kuaidaili.password}@{proxy}/"
            }
            return proxies
        elif self.proxy_type == ZHIMA:
            proxy = self.zhima.get_proxy(num=1)
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            return proxies

    def get_proxy_selenium(self):

        if self.proxy_type == KYAIDAILI:
            proxy = self.kuaidaili.get_dps()
            proxy_info = {
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1],
                'username': self.kuaidaili.username,
                'password': self.kuaidaili.password
            }
            return proxy_info
        elif self.proxy_type == ZHIMA:
            proxy = self.zhima.get_proxy(num=1)
            proxy_info = {
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1],
            }
            return proxy_info
