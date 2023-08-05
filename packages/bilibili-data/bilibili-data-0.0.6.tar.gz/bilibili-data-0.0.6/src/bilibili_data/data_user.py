import asyncio
from bilibili_api import video, user


class VideoFilter:
    def __init__(self):
        self.cache = self.load_cache()

    def load_cache(self):
        """加载数据库缓存"""
        return {}

    def filter(self, bvid='', play=0, comment=0, created=0, video_review=0):
        """返回值为True，则不更新视频缓存数据"""
        return False


class User:
    def __init__(self, uid: int, sleep_sec=0.5, video_filter=VideoFilter()):
        self.up = user.User(uid=uid)
        self.sleep_sec = sleep_sec
        self.videos = []
        self.video_filter = video_filter

    async def get_videos(self):
        """获取用户发布的所有视频"""
        pn = 1
        self.videos = []
        while True:
            info = await self.up.get_videos(pn=pn)
            page = info['page']
            vlist = info['list']['vlist']
            for v_info in vlist:
                await asyncio.sleep(self.sleep_sec)
                video_info = {
                    'comment': v_info['comment'],
                    'play': v_info['play'],
                    'description': v_info['description'],
                    'title': v_info['title'],
                    'author': v_info['author'],
                    'mid': v_info['mid'],
                    'created': v_info['created'],
                    'length': v_info['length'],
                    'video_review': v_info['video_review'],
                    'aid': v_info['aid'],
                    'bvid': v_info['bvid'],
                }
                if self.video_filter.filter(bvid=v_info['bvid'], play=v_info['play'], comment=v_info['comment'],
                                            created=v_info['created'], video_review=v_info['video_review']):
                    continue
                print(f'\r正在解析视频：{video_info["title"]}', end='')
                v = video.Video(bvid=video_info['bvid'])
                v_info = await v.get_info()
                video_info['duration'] = v_info['duration']
                video_info['stat'] = v_info['stat']
                self.videos.append(video_info)
            if page['pn'] * page['ps'] > page['count']:
                break
            pn += 1
        print('\n')
        return self.videos
