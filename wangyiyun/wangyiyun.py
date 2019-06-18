from lxml import etree
import requests, os, sys, click, re
from http import cookiejar
from encrypyed import Encrypyed


class Cralwer:
    """
    下载网易云音乐的类
    """

    def __init__(self, timeout=60, cookie_path='.'):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_url(self, url, params):
        """
        将params编码，并提交url，获取json数据
        :param url:
        :param params:
        :return:
        """
        data = self.ep.encrypted_request(params)
        resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        if result['code'] != 200:
            print("post_url error")
        else:
            return result

    def get_song_id(self, song_name, search_type=1, limit=9):
        """
        通过歌名获取歌曲的id号
        :param song_name:
        :param search_type:
        :param limit:
        :return:
        """
        url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token"
        params = {'s': song_name, 'type': search_type, 'offset': 0, 'sub': 'false', 'limit': limit}
        result = self.post_url(url, params)
        return result

    def get_song_url(self, song_id, bit_rate=320000, csrf=''):
        """
        通过id号获取歌曲的下载链接
        :param song_id: 歌曲id
        :param bit_rate: 音质
        :param csrf: csrf_token
        :return:
        """
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.post_url(url, params)
        # 歌曲下载地址
        song_url = result['data'][0]['url']

        # 歌曲不存在
        if song_url is None:
            click.echo('Song {} is not available due to copyright issue.'.format(song_id))
        else:
            return song_url

    def download_song(self, url, song_name, folder):
        """
        下载歌曲
        :param url:
        :param song_name:
        :param folder:
        :return:
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        fpath = os.path.join(folder, song_name + '.mp3')
        if sys.platform == "win32" or sys.platform == 'cygwin':
            valid_name = re.sub(r'[<>:"/\\|?*]', '', song_name)
            if valid_name != song_name:
                click.echo("{} will be saved as: {}.mp3".format(song_name, valid_name))
                fpath = os.path.join(folder, valid_name + '.mp3')
        if not os.path.exists(fpath):
            resp = self.download_session.get(url, timeout=self.timeout, stream=True)
            length = int(resp.headers.get('content-length'))
            label = 'Downloading {} {}kb'.format(song_name, int(length / 1024))

            with click.progressbar(length=length, label=label) as progressbar:
                with open(fpath, 'wb') as song_file:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            song_file.write(chunk)
                            progressbar.update(1024)

    def download_by_playlist(self, url):
        folder = "Musics"
        ids = self.get_ids_by_url(url)
        for id in ids[:10]:
            song_url = self.get_song_url(id)
            print(song_url)
            self.download_song(song_url, id, folder)

    def get_ids_by_url(self, url):
        resp = self.session.get(url)
        s = "/song\?id=(\\d{5,11})"
        pattern = re.compile(s)
        ids = re.findall(pattern, resp.text)
        return ids


if __name__ == '__main__':
    crawler = Cralwer()
    # url = "https://music.163.com/playlist?id=554019970"
    url = "https://music.163.com/playlist?id=2783351162"
    crawler.download_by_playlist(url)
    # id = "1370858195"
    # crawler.get_name_by_id(id)
