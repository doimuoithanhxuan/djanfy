import glob
from pathlib import Path
from threading import Thread
from typing import Dict, Type

from django.conf import settings
from youtube_dl import YoutubeDL

from player.models import Song


class CustomYoutubeDL(YoutubeDL):
    """
    Inherited class from YoutubeDL force only download audios at Soundcloud, Youtube.
    Usage:
    >>> params = {'format': 'bestaudio/best',
    >>>          'ignoreerrors': True,
    >>>          'prefer_ffmpeg': True,
    >>>          'outtmpl': '%(id)s.%(ext)s',
    >>>          'postprocessors': [{'key': 'FFmpegExtractAudio',
    >>>            'preferredcodec': 'best',
    >>>            'preferredquality': '5',
    >>>            'nopostoverwrites': False}]
    >>> }
    >>> url = "https://www.youtube.com/watch?v=Ls6EBIR8hDE"
    >>> dl = CustomYoutubeDL(params)
    >>> dl.download(url)
    >>> # Or use with context manager
    >>> with CustomYoutubeDL(params) as dl:
    >>>  dl.download(url)
    >>>
    """

    def __init__(self, **kwargs):
        self.base_params = {
            "format": "bestaudio/best",
            "ignoreerrors": True,
            "prefer_ffmpeg": True,
            "noplaylist": True,
            "outtmpl": str(settings.MEDIA_ROOT) + "/%(id)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "best",
                    "preferredquality": "5",
                    "nopostoverwrites": False,
                }
            ],
        }
        super().__init__(auto_init=False, params=self.base_params)
        self.custom_extractors = [
            "Youtube",
            "YoutubeYtBe",
            "Soundcloud",
            "YoutubePlaylist",
            "YoutubeTab",
            "SoundcloudSet",
            "SoundcloudUser",
            "SoundcloudTrackStation",
            "SoundcloudPlaylist",
        ]
        self._ies = [self.get_info_extractor(ie_key) for ie_key in self.custom_extractors]

    def get_ie_result(self, url: str, process=True, download=False):
        """
        Get info about url without download it.
        """
        return self.extract_info(url, download=download, process=process)

    def download_video_with_ie_result(self, ie_result):
        return self.process_ie_result(ie_result)


class DownloadInThread(Thread):
    def __init__(self, ytdl: Type[CustomYoutubeDL], ie_result: Dict, song: Type[Song]):
        self.ytdl = ytdl
        self.ie_result = ie_result
        self.song = song
        super().__init__()

    @staticmethod
    def get_file(song_id):
        file_pattern = str(settings.MEDIA_ROOT) + f"/{song_id}.*"
        return glob.glob(file_pattern)[0]

    def run(self):
        try:
            self.ytdl.download_video_with_ie_result(ie_result=self.ie_result)
            status = "success"
            file = self.get_file(self.song.song_id)
            self.song.file = file
            self.song.file.name = Path(file).name
        except Exception:
            status = "fail"
        finally:
            self.song.status = status
            self.song.save()
