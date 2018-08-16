# kamerowanie

Ever wanted to put your camera(s) feed on your website? Tired of overpriced services that offer such thing?
Then this little script is for you - it converts RTSP stream into HLS (HTTP Live Streaming) format using ffmpeg and more!

### Prerequisites

Before you use my script you need a build of [ffmpeg](https://www.ffmpeg.org/). If you're using Windows, you might consider adding bin folder to your PATH.

### Basic Usage

Run this script with at least Python 3.6 passing two arguments:
- cam_key: it's just a name of folder script will create to work on
- rtsp_adress: your camera's rtsp address e.g. rtsp://127.0.0.1:554/stream

```
python3 preview.py bigbuckbunny rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov
```

Then, script will create your main project directory which will look like that:
    .
    ├── kamerowanie                   # Main path
    │   ├── bigbuckbunny              # Camera directory name (cam_key)
    │   │   ├── live                  # Directory to store processed stream (HLS files)
    │   │   │   ├── index.m3u8        # Index file which stores most recent segment (.ts file)
    │   │   │   └── ...               # Segment files (.ts files)
    │   │   ├── start.sh              # Script which grabs camera feed and transcodes it into HLS format
    │   │   ├── pid.txt               # PID of ffmpeg
    └── ...                           # Other cameras
    
Then you can share this directory using http server or a websocket.
e.g.
```
python3 -m http.server
```

At last, you can choose any video player plugin that support HLS, I've only tested [video.js](https://github.com/videojs/video.js) + [videojs-contrib-hls](https://github.com/videojs/videojs-contrib-hls).

### Configuration

You might consider configuring some variables.

```ffmpeg_path``` - if u don't want to store ffmpeg in your PATH variable, you might want to pass it your ffmpeg path
```main_path``` - this is where you store your camera directories, usually /var/www/static/cameras
```log_path``` - this is where you store logs, usually /var/www/static/cameras/log.log
