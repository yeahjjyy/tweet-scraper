import json
import string
import zipfile

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from browser.proxy.proxy import *
from browser.utils.ip_handler import *
from browser.utils.user_agent import *
from logger import logger
from configs.configs import *

import platform


class BaseBrowser:
    def __init__(self, options=None, browser=None):
        if options:
            self.options = options
        else:
            self.options = Options()
        self.browser = browser

    def wait_element(self, element_id, wait_time=15):
        try:
            WebDriverWait(self.browser, wait_time, 1).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except Exception as e:
            logger.error(f'[wait_element] wait timeout, error: {e}')
            raise

    def wait_element_css(self, css, wait_time=15):
        try:
            WebDriverWait(self.browser, wait_time, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css))
            )
        except Exception as e:
            logger.error(f'[wait_element_css] wait timeout, error: {e}')
            raise

    def wait_element_xpath(self, xpath, wait_time=15):
        try:
            WebDriverWait(self.browser, wait_time, 1).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            logger.error(f'[wait_element_xpath] wait timeout, error: {e}')
            raise

    def add_header(self, headers):
        for k, v in headers.items():
            self.options.add_argument(f'{k}={v}')

    def load_cookies(self, url, cookies, refresh=False):
        """
        Loading cookies. When loading, I need to put my corresponding website first, otherwise the cookies cannot be loaded normally.
        https://x.com/
        :param url
        :param cookies: selenium.get_cookies()
        :param refresh
        :return:
        """
        self.browser.get(url)
        for c in cookies:
            self.browser.add_cookie(c)
        if refresh:
            self.browser.refresh()

    def disable_img_css(self):
        # 禁止图片
        prefs = {"profile.managed_default_content_settings.images": 2,
                 }
        self.options.add_experimental_option("prefs", prefs)

    def disable_css(self):
        # 禁止css加载
        prefs = {'permissions.default.stylesheet': 2}
        self.options.add_experimental_option("prefs", prefs)

    def browser_headless(self):
        # 无头浏览器
        self.options.add_argument('headless')

    def create_proxyauth_extension(self, proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                   plugin_path=None):
        """

        :param proxy_host
        :param proxy_port
        :param proxy_username
        :param proxy_password
        :param scheme
        :param plugin_path
        :return:
        """

        if plugin_path is None:
            plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return plugin_path

    def process_browser_logs_for_network_events(self, logs):
        """
        Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
        since we're interested in the network events specifically.
        """
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.response" in log["method"]
                    or "Network.request" in log["method"]
                    or "Network.webSocket" in log["method"]
            ):
                yield log

    def get_browser(self, disable_img=False, disable_css=False, headless=False, proxy_info=None, script_files=None, record_network_log=None):
        """
        get browser
        :param disable_img
        :param disable_css
        :param headless
        :param proxy_info
            proxy_info: {
                ip,
                port,
                username,
                password,
                type
            }
        :param script_files
        :param record_network_log
        :return:
        """

        # # hidden webdriver feature
        # self.options.add_argument("disable-blink-features=AutomationControlled")
        # # open developer model, in this model, webdriver attribute is normal
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.options.add_experimental_option('useAutomationExtension', False)
        # self.options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')

        user_agent = get_user_agent()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        self.add_header(headers)
        if headless:
            self.browser_headless()
        if disable_img:
            self.disable_img_css()
        if disable_css:
            self.disable_css()

        # set proxy
        if proxy_info:
            proxy_type = proxy_info.get('proxy_type', KYAIDAILI)
            if proxy_type == KYAIDAILI:
                # proxy need username and password, selenium need plug to supple this.
                # https://www.kuaidaili.com/doc/dev/sdk_http/#chrome
                proxyauth_plugin_path = self.create_proxyauth_extension(
                    proxy_host=f"{proxy_info['ip']}",  # proxy ip
                    proxy_port=f"{proxy_info['port']}",  # proxy port
                    proxy_username=f"{proxy_info['username']}",
                    proxy_password=f"{proxy_info['password']}"
                )
                self.options.add_extension(proxyauth_plugin_path)
            elif proxy_type == ZHIMA:
                ip = proxy_info['ip']
                port = proxy_info['port']
                proxy = f'{ip}:{port}'
                self.options.add_argument('--proxy-server=%s' % proxy)
        os_name = platform.system()
        if os_name == 'Windows':
            path = os.path.join(root_path, 'browser', 'chromedriver.exe')
        elif os_name == 'Darwin':
            path = os.path.join(root_path, 'browser', 'chromedriver')
        else:
            path = os.path.join(root_path, 'browser', 'chromedriver')
        if record_network_log:
            # https://gist.github.com/rengler33/f8b9d3f26a518c08a414f6f86109863c
            # capabilities = DesiredCapabilities.CHROME
            # capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
            # capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
            self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
            service = Service(executable_path=path)
            browser = webdriver.Chrome(service=service, options=self.options)

        else:
            service = Service(executable_path=path)
            browser = webdriver.Chrome(service=service, options=self.options)


        defalut_script_files = [
            'stealth.min.js',  # hidden selenium feature
        ]
        if script_files:
            script_files.extend(defalut_script_files)
        else:
            script_files = defalut_script_files
        for sf in script_files:
            js_path = os.path.join(root_path, 'browser', 'js', sf)
            with open(js_path, encoding='utf-8') as f:
                js = f.read()
            # execute javascript before webpage open
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })

        if proxy_info:
            ip = proxy_info['ip']
            res_json = get_timezone_geolocation(ip)
            geo = {
                "latitude": res_json.get('lat', 116.480881),
                "longitude": res_json.get('lon', 39.989410),
                "accuracy": 1
            }
            # Default timezone is Shanghai
            tz = {
                "timezoneId": res_json.get('timezone', 'Asia/Shanghai')
            }
            browser.execute_cdp_cmd("Emulation.setGeolocationOverride", geo)
            browser.execute_cdp_cmd("Emulation.setTimezoneOverride", tz)

        browser.implicitly_wait(15)

        return browser
