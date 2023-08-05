import asyncio
from bilibili_api import video, user


class User:
    def __init__(self, uid: int, sleep_sec=0.5):
        self.up = user.User(uid=uid)
        self.sleep_sec = sleep_sec
        self.videos = []

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
