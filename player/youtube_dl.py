from youtube_dl import YoutubeDL


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

    def __init__(self, *args, **kwargs):
        super().__init__(auto_init=False, *args, **kwargs)
        self.custom_extractors = [
            "Youtube",
            "YoutubeYtBe",
            "Soundcloud",
            "YoutubePlaylist",
            "SoundcloudPlaylist",
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
