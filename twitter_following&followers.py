
import json

import time
import traceback


from selenium.webdriver import Keys, ActionChains


from browser.base_browser import BaseBrowser
from browser.utils.canvas import modify_random_canvas_js
from selenium import webdriver

from browser.utils.user_agent import get_user_agent


# 定义自定义异常类
class RateLimitExceededException(Exception):
    pass


class TwitterFollowing(BaseBrowser):

    def __init__(self, user_data_dir='C:/Users/USER/Desktop/work_content/user-data10/',
                 remote_debugging_port=9223) -> None:
        super().__init__()
        self.options = webdriver.ChromeOptions()
        user_agent = get_user_agent()
        self.options.add_argument(f'user-agent={user_agent}')

        # prefs = {
        #     "profile.managed_default_content_settings.images": 2,  # disable image
        #     "profile.managed_default_content_settings.plugins": 2,  # disable plugins（include video）
        #     "profile.managed_default_content_settings.media_stream": 2  # disable media_stream（eg:video）
        # }
        # self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument(f"--user-data-dir={user_data_dir}")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument(f"--remote-debugging-port={remote_debugging_port}")

        # for debug
        # self.options.add_experimental_option("debuggerAddress", "localhost:9223")

        js_script_name = modify_random_canvas_js()
        self.browser = self.get_browser(script_files=[js_script_name], record_network_log=True, headless=True)

    def scroll_once(self, distance=2000):
        actions = ActionChains(self.browser)
        actions.scroll_by_amount(0, distance).perform()

    def twitter_following(self, type: str):

        result_list = []

        self.browser.switch_to.new_window('tab')
        if type == 'BlueVerifiedFollowers':
            url = 'https://x.com/i/api/graphql/UdtZY8FOW3ULVnjDU52BVg/BlueVerifiedFollowers'
        elif type == 'Following':
            url = 'https://x.com/i/api/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName'
        elif type == 'FollowersYouKnow':
            url = "https://x.com/i/api/graphql/JDcfgeQj5nyNGGRk46JM5w/FollowersYouKnow"
        else:
            url = 'https://x.com/i/api/graphql/eWTmcJY3EMh-dxIR7CYTKw/Following'
        self.browser.get(url=url)

        time.sleep(2)

        exist_entry_id = []

        self.get_network(exist_entry_id, result_list)

        print(f'tweet result length = {len(result_list)}')

    def get_network(self, exist_entry_id, result_list):
        performance_log = self.browser.get_log("performance")

        for packet in performance_log:

            msg = packet.get("message")
            message = json.loads(packet.get("message")).get("message")
            packet_method = message.get("method")

            if "Network" in packet_method and 'Following' in msg:

                request_id = message.get("params").get("requestId")
                try:
                    print("request_id=" + request_id)
                    try:
                        resp = self.browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    except Exception as e2:
                        time.sleep(1)
                        resp = self.browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})

                    body = resp.get("body")
                    body = json.loads(body)
                    instructions = body['data']['user']['result']['timeline']['timeline'].get('instructions', None)
                    if not instructions:
                        continue
                    for instruction in instructions:
                        entries = instruction.get('entries', None)
                        if entries:
                            for entry in entries:
                                user_info = {}
                                content = entry['entryId']
                                if content not in exist_entry_id:
                                    exist_entry_id.append(content)
                                else:
                                    continue
                                if 'cursor-' in content:
                                    continue

                                body = entry['content']['itemContent']['user_results'].get('result', None)
                                if not body:
                                    continue
                                user_info['userId'] = body['rest_id']
                                user_info['isBlueVerified'] = body['is_blue_verified']
                                user_info['following'] = body['legacy']['following']
                                user_info['canDm'] = body['legacy']['can_dm']
                                user_info['canMediaTag'] = body['legacy']['can_media_tag']
                                user_info['createdAt'] = body['legacy']['created_at']
                                user_info['defaultProfile'] = body['legacy']['default_profile']
                                user_info['defaultProfileImage'] = body['legacy']['default_profile_image']
                                user_info['description'] = body['legacy']['description']
                                user_info['description'] = body['legacy']['description']
                                user_info['fastFollowersCount'] = body['legacy']['fast_followers_count']
                                user_info['favouritesCount'] = body['legacy']['favourites_count']
                                user_info['followersCount'] = body['legacy']['followers_count']
                                user_info['friendCount'] = body['legacy']['friends_count']
                                user_info['hasCustomTimelines'] = body['legacy']['has_custom_timelines']
                                user_info['isTranslator'] = body['legacy']['is_translator']
                                user_info['listedCount'] = body['legacy']['listed_count']
                                user_info['location'] = body['legacy']['location']
                                user_info['mediaCount'] = body['legacy']['media_count']
                                user_info['name'] = body['legacy']['name']
                                user_info['normalFollowersCount'] = body['legacy']['normal_followers_count']
                                user_info['pinnedTweetIdsStr'] = body['legacy']['pinned_tweet_ids_str']
                                user_info['possiblySensitive'] = body['legacy']['possibly_sensitive']
                                user_info['profileImageUrlHttps'] = body['legacy']['profile_image_url_https']
                                user_info['profileInterstitialType'] = body['legacy']['profile_interstitial_type']
                                user_info['username'] = body['legacy']['screen_name']
                                user_info['statusesCount'] = body['legacy']['statuses_count']
                                user_info['translatorType'] = body['legacy']['translator_type']
                                user_info['verified'] = body['legacy']['verified']
                                user_info['wantRetweets'] = body['legacy']['want_retweets']
                                user_info['withheldInCountries'] = body['legacy']['withheld_in_countries']
                                result_list.append(user_info)
                                print(user_info)
                except Exception as e:
                    print('error', e)
                    if not isinstance(e, RateLimitExceededException):
                        print(f"Caught a non-RateLimitExceededException error: {e}")
                    else:
                        print('error', e)
                        raise e
                    print(e)
                    traceback.print_exc()
                    pass


if __name__ == '__main__':
    twitter = TwitterFollowing()
    url = "https://x.com/explore"
    twitter.browser.get(url=url)
    # set Cookie https://1-usd-promotion.com/how-to-get-auth-token
    cookie = {
        'name': 'auth_token',
        'value': '',
        'domain': '.x.com'
    }

    twitter.browser.add_cookie(cookie)

    time.sleep(0.1)
    result = twitter.twitter_following()
    print(result)

# output
# {'userId': '1350150750966603777', 'isBlueVerified': True, 'following': False, 'canDm': False, 'canMediaTag': False, 'createdAt': 'Fri Jan 15 18:40:52 +0000 2021', 'defaultProfile': True, 'defaultProfileImage': False, 'description': 'Husband, dad, (very) amateur guitarist, and the 71st Secretary of State serving under the leadership of @POTUS Biden.', 'fastFollowersCount': 0, 'favouritesCount': 5, 'followersCount': 2280106, 'friendCount': 55, 'hasCustomTimelines': False, 'isTranslator': False, 'listedCount': 7984, 'location': '', 'mediaCount': 2702, 'name': 'Secretary Antony Blinken', 'normalFollowersCount': 2280106, 'pinnedTweetIdsStr': [], 'possiblySensitive': False, 'profileImageUrlHttps': 'https://pbs.twimg.com/profile_images/1363277550928158722/LzlIxuhQ_normal.jpg', 'profileInterstitialType': '', 'username': 'SecBlinken', 'statusesCount': 5946, 'translatorType': 'none', 'verified': False, 'wantRetweets': False, 'withheldInCountries': []}