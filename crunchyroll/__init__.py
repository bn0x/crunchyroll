import requests

class Crunchyroll:
    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        if self.login():
            self.authenticated = True
        else:
            print("Failed to log into crunchyroll lol")
            self.authenticated = False
            return

    def login(self):
        iNeedASession = self.session.post('http://api.crunchyroll.com/start_session.0.json',
                                           data={
                                                'device_type': 'com.crunchyroll.winphone',
                                                'access_token': 'z6J2faQjApno1A1',
                                                'device_id': 'hacks',
                                                'version': '1.3.0.0',
                                                'fields': 'user.username,user.premium,user.email',
                                           })
        self.session_id = iNeedASession.json()['data']['session_id']
        loginRequest = self.session.post("https://api.crunchyroll.com/login.0.json",
                                data={
                                    'session_id': self.session_id,
                                    'account': self.username,
                                    'password': self.password,
                                    'fields': 'user.username,user.premium,user.email',
                                    'locale': 'enUS',
                                })
        if loginRequest.json()['code'] == 'ok':
            self.auth = loginRequest.json()['data']['auth']
            return True
        else:
            return False

    def batch(self):
        return self.session.post('https://api.crunchyroll.com/batch.0.json',
                                 data={
                                    'session_id': self.session_id,
                                    'requests': '[{"method":"POST","api_method":"list_series","method_version":0,"params":{"media_type":"anime","filter":"popular","limit":"50","fields":"series.series_id,series.name,series.media_count,series.collection_count,series.description,series.portrait_image,series.in_queue,image.medium_url"}},{"method":"POST","api_method":"list_series","method_version":0,"params":{"media_type":"anime","filter":"simulcast","limit":"100","fields":"series.series_id,series.name,series.media_count,series.collection_count,series.description,series.portrait_image,series.in_queue,image.medium_url"}},{"method":"POST","api_method":"list_series","method_version":0,"params":{"media_type":"anime","filter":"alpha","limit":"50","fields":"series.series_id,series.name,series.media_count,series.collection_count,series.description,series.portrait_image,series.in_queue,image.medium_url"}},{"method":"POST","api_method":"list_series","method_version":0,"params":{"media_type":"anime","filter":"updated","limit":"50","fields":"series.series_id,series.name,series.media_count,series.collection_count,series.description,series.landscape_image,series.portrait_image,series.in_queue,series.most_recent_media,media.available_time,media.episode_number,image.medium_url"}}]',
                                    'locale': 'enUS',
                                 }).json()

    def get_episodes(self, *args, **kwargs):
        return self.session.post('https://api.crunchyroll.com/batch.0.json',
                                 data={
                                    'session_id': self.session_id,
                                    'requests': '[{"method":"POST","api_method":"list_ads","method_version":0,"params":{"format":"vast","placement":"preroll"}},{"method":"POST","api_method":"info","method_version":0,"params":{"media_id":%s,"fields":"media.stream_data,media.ad_spots"}}]'%kwargs['media_id'],
                                    'locale': 'enUS',
                                 }).json()

    def info(self, *args, **kwargs):
        return self.session.post('https://api.crunchyroll.com/info.0.json',
                                  data={
                                    'session_id': self.session_id,
                                    'series_id': kwargs['series_id'],
                                    'fields': 'series.series_id,series.media_count,series.description,series.year,series.publisher_name',
                                    'locate': 'enUS',
                                  }).json()

    def list_collections(self, *args, **kwargs):
        kwargs.setdefault('session_id', self.session_id)
        kwargs.setdefault('sort', 'desc')
        kwargs.setdefault('limit', 100)
        kwargs.setdefault('fields', 'collection.collection_id,collection.name,collection.season')
        kwargs.setdefault('locale', 'enUS')
        return self.session.post('https://api.crunchyroll.com/list_collections.0.json',
                                  data=kwargs).json()


    def list_media(self, *args, **kwargs):
        kwargs.setdefault('session_id', self.session_id)
        kwargs.setdefault('fields', 'media.media_id,media.media_type,media.episode_number,media.name,media.screenshot_image,media.available,media.premium_only,media.series_name,media.description,media.available_time,image.wide_url,image.widestar_url')
        kwargs.setdefault('locate', 'enUS')
        kwargs.setdefault('sort', 'desc')
        kwargs.setdefault('limit', 500)
        return self.session.post('https://api.crunchyroll.com/list_media.0.json',
                                  data=kwargs).json()