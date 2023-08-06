import requests

class KyLy:
    def __init__(self, token: str=None, group_guild=None):
        try:
            self.token = token
            self.group_guild = group_guild
            self.headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            self.base_url = 'https://api-ssl.bitly.com'
        except Exception as ex:
            print(ex)

    def shorten(self, link: str=None, domain: str='bit.ly') -> str:
        try:
            if not self.group_guild:
                data = '{ "long_url": "%s","domain": "%s" }' %(link, domain)

                shortened_url = requests.post(self.base_url + '/v4/shorten', headers=self.headers, data=data).json()
                shortened_url = shortened_url['link']

            else:
                data = '{ "long_url": "%s","domain": "%s", "group_guild": "%s"}' %(link, domain, self.group_guild)

                shortened_url = requests.post(self.base_url + '/v4/shorten', headers=self.headers, data=data).json()
                shortened_url = shortened_url['link']

            return shortened_url
        except Exception as ex:
            print(ex)

    def update_link(self, bitlink, new_link_url,domain: str='bit.ly') -> str:
        try:
            if not self.group_guild:
                data = '{ "long_url": "%s","domain": "%s" }' %(new_link_url, domain)

                new_url = requests.patch(self.base_url + f'/v4/bitlinks/{bitlink}', headers=self.headers, data=data).json()

                new_url = new_url['link']

            else:
                data = '{ "long_url": "%s","domain": "%s", "group_guild": "%s" }' %(new_link_url, domain, self.group_guild)

                new_url = requests.patch(self.base_url + f'/v4/bitlinks/{bitlink}', headers=self.headers, data=data).json()

                new_url = new_url['link']

            return new_url
        except Exception as ex:
            print(ex)

    def link_information(self, link: str) -> dict:
        try:
            information = requests.get(self.base_url + f'/v4/bitlinks/{link}', headers=self.headers).json()

            return information
        except Exception as ex:
            print(ex)

    def expand(self, bitlink: str) -> str:
        try:
            data = '{"bitlink_id": "%s"}' %bitlink
            expanded_link = requests.post(self.base_url + '/v4/expand', headers=self.headers, data=data).json()

            return expanded_link['long_url']
        except Exception as ex:
            print(ex)

    def click(self, bitlink: str, unit: str='day', units:int=-1) -> dict:
        try:
            params = (('unit',unit), ('units',units))
            response = requests.get(self.base_url + f'/v4/bitlinks/{bitlink}/clicks', headers=self.headers, params=params).json()

            return response
        except Exception as ex:
            print(ex)

    def click_summary(self, bitlink:str, unit:str='day', units:int=-1) -> dict:
        try:
            params = (('unit',unit), ('units',units))
            response = requests.get(self.base_url + f'/v4/bitlinks/{bitlink}/clicks/summary', headers=self.headers, params=params).json()

            return response
        except Exception as ex:
            print(ex)
