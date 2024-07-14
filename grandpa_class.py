import requests
import os
from dotenv import load_dotenv
from lxml import html
import json


load_dotenv()
Email = os.getenv('Email')
Password = os.getenv('Password') # through API
access_API = os.getenv('API_key') # through API
API_key = os.getenv('API_key')
dashboard_url = "https://jagadguru.siddhamahayog.org/user/dashboard"
login_url = "https://jagadguru.siddhamahayog.org/login"
dataPacket = {}


if(access_API == API_key):
    dataPacket['API_auth'] = True
    initial_rsp = requests.get(url=login_url)
    dataPacket['site_status_code'] = initial_rsp.status_code
    if(initial_rsp.status_code == 200):
        siddha_session = initial_rsp.cookies.get('siddhamahayog_session')
        XSRF_session = initial_rsp.cookies.get('XSRF-TOKEN')


        site_session = requests.Session()
        site_session.headers.update({
            'XSRF-TOKEN': XSRF_session,
            'siddhamahayog_session': siddha_session,
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Host': 'jagadguru.siddhamahayog.org'
        })
        login_header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Content-Length': '877',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'siddhamahayog_session={siddha_session}; XSRF-TOKEN={XSRF_session}',
            'Origin': 'https://jagadguru.siddhamahayog.org',
            'Referer': 'https://jagadguru.siddhamahayog.org/login',
            'Sec-Fetch-Dest': 'document'
        }
        login_payload = {
            '_token': XSRF_session,
            'email': Email,
            'password': Password
        }
        login_rsp = site_session.post(login_url, headers=login_header, data=login_payload)
        new_siddha_session = login_rsp.cookies.get('siddhamahayog_session')
        new_XSRF_session = login_rsp.cookies.get('XSRF-TOKEN')


        if((siddha_session != new_siddha_session) and (XSRF_session != new_XSRF_session)):
            dataPacket['login'] = True
            logged_in_header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                'Cookie': f'siddhamahayog_session={new_siddha_session}; XSRF-TOKEN={new_XSRF_session}',
                'Sec-Fetch-Dest': 'document'
            }
            site_session.headers.update({
                'XSRF-TOKEN': new_XSRF_session,
                'siddhamahayog_session': new_siddha_session
            })
            dashboard_rsp = site_session.get(url=dashboard_url, headers=logged_in_header)
            tree = html.fromstring(dashboard_rsp.text)
            url_xpath = '//div[@class="card-body"]//li[2]//button[1]'
            element = tree.xpath(url_xpath)
            element_attr = element[0].attrib
            if(element_attr.get('data-action')):
                dataPacket['class'] = True
                needed_url = element_attr.get('data-action')
                meeturl_header = {
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cache-Control': 'no-cache',
                    'Content-Length': '0',
                    'Cookie': f'XSRF-TOKEN={new_XSRF_session}; siddhamahayog_session={new_siddha_session} ',
                    'Origin': 'https://jagadguru.siddhamahayog.org',
                    'Pragma': 'no-cache',
                    'Referer': 'https://jagadguru.siddhamahayog.org/user/dashboard',
                    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                    'Sec-Ch-Ua-Mobile': '?0',
                    'Sec-Ch-Ua-Platform': '"Windows"',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                    'X-Csrf-Token': new_XSRF_session,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                response4 = site_session.post(url=needed_url, headers=meeturl_header)
                response_json = response4.json()
                dataPacket['zoom_url'] = response_json['params']['location']
            else:
                dataPacket['class'] = False
        else:
            dataPacket['login'] = False
else:
    dataPacket['API_auth'] = False


print(dataPacket) #JSON MA YO DATAPACKET RETURN