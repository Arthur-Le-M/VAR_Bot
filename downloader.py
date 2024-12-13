import youtube_dl

class Downloader:
    def __init__(self, src="playlist.txt", path="./downloads") -> None:
        self.src = src
        self.path = path

    def download_hook(self, d):
        """give the percentage of downloading"""
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
            print(f"Download progress: {percent_str}")

    def download_dailymotion_videos_from_playlist(self):
        """read playlist and download videos"""
        with open(self.src, 'r') as file:
            video_urls = file.readlines()
        
        ydl_opts = {
            'outtmpl': f'{self.path}/%(autonumber)02d - %(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'progress_hooks': [self.download_hook],

            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }
            ]
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for video_url in video_urls:
                ydl.download([video_url.strip()])
                print(f"Video from {video_url.strip()} downloaded successfully!")