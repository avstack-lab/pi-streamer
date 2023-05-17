#!/usr/bin/python3
import argparse
import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput


def main(args):
    dt_min = int(1e6 / args.framerate)
    dt_max = int(1e6 / args.framerate)
    picam2 = Picamera2()
    main_ = {
        "size": (args.width, args.height),
    }
    controls = {"FrameDurationLimits": (dt_min, dt_max)}
    video_config = picam2.create_video_configuration(main=main_, controls=controls)
    picam2.configure(video_config)
    encoder = H264Encoder(1000000)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((args.dest_address, args.dest_port))
        stream = sock.makefile("wb")
        print("starting recording")
        picam2.start_recording(encoder, FileOutput(stream))
        try:
            while True:
                time.sleep(20)
        except Exception as e:
            print("ending recording")
            picam2.stop_recording()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--framerate", type=int, default=30, help="video framerate")
    parser.add_argument("--width", type=int, default=1920, help="image width")
    parser.add_argument("--height", type=int, default=1080, help="image height")
    parser.add_argument(
        "--dest_address", type=str, required=True, help="ip address to stream to"
    )
    parser.add_argument(
        "--dest_port", type=int, required=True, help="port number to stream to"
    )

    args = parser.parse_args()
    main(args)
