import subprocess
import sys
import logging

from time import sleep
from pathlib import Path

# ffmpeg command which is called to start streaming new camera through rtsp address
# i've decided to use hls muxer to be able to easily get rid of old segments
# it generates index (.m3u8) file which containts information about active segments
# which then is used to display video on page using videojs and videojs-hls plugin.
# You can customize it as you want, of course.
cmd = "{} -loglevel panic -hide_banner -nostats -fflags nobuffer -rtsp_transport tcp -i {} -vsync 0 " \
      "-copyts -vcodec copy -movflags frag_keyframe+empty_moov -an " \
      "-f hls -hls_flags delete_segments+append_list -hls_time 1 -hls_list_size 5 " \
      "-hls_delete_threshold 30 -hls_segment_filename {} {}"
# If ffmpeg is not in your PATH variable then you should set absolute path to ffmpeg here.
ffmpeg_path = Path("ffmpeg")
# This is should be your www/static path.
main_path = Path("/home/kamerowanie/camera")
# Path to store log file
log_path = Path("/home/kamerowanie/camera/log.log")

script = """#!/bin/bash
{} & echo $! > {}
"""

def main(cam_key, rtsp_address):
    pid = 0
    # -- Camera directory
    logging.info("  Creating camera directory...")
    cam_path = main_path / cam_key
    index_path = Path(cam_path / "live" / "index.m3u8")
    segment_path = Path(cam_path / "live" / "%01d.ts")
    if cam_path.exists():
        logging.error("    Directory %s already exists!" % cam_key)
        raise RuntimeError
    try:
        cam_path.mkdir()
    except:
        logging.error("    Couldn't create camera directory!")
        raise
    Path(cam_path / "live").mkdir()
    logging.info("  Created directory on path %s" % cam_path)
    # -- Converting script
    logging.info("  Creating converting script...")
    try:
        with open(str(Path(cam_path / "start.sh")), "w") as f:
            f.write(
                script.format(
                    cmd.format(ffmpeg_path, rtsp_address, segment_path, index_path),
                    str(cam_path / "pid.txt")
                )
            )
    except:
        logging.error("    Couldn't create converting script!")
        raise
    Path(cam_path / "start.sh").chmod(0o777)
    # -- -- Running converting script
    logging.info("  Running converting script...")
    try:
        subprocess.Popen(str(Path(cam_path / "start.sh")), shell=True, stdout=subprocess.DEVNULL)
    except:
        logging.error("    Couldn't run converting script!")
        raise
    # -- -- Getting pid
    # Sleep 3 seconds to give ffmpeg time to initialize
    sleep(3) 
    try:
        with open(str(Path(cam_path / "pid.txt"))) as f:
            pid = f.read()
    except:
        logging.error("Couldn't get PID!")
        raise
    # -- Last log
    logging.info("LIVE: RTSP:{} PATH:{} PID:{}".format(rtsp_address, cam_path, pid))


if __name__ == "__main__":
    if not main_path.exists():
        x = input("Main path doesn't exist Create it?\n[Y]/[N]: ")[0].lower()
        if x == 'y':
            main_path.mkdir()
        else:
            raise RuntimeError("Main path was not created!")
    logging.basicConfig(format='[%(asctime)s]<%(levelname)s>: %(message)s', filename=str(log_path), level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')
    logging.info("Registering a new camera...")
    if len(sys.argv) != 3:
        logging.error("  Cam key or cam address was not provided!")
        raise RuntimeError
    logging.info("  Configuring camera with key: %s and address: %s..." % (sys.argv[1], sys.argv[2]))
    main(sys.argv[1], sys.argv[2])
