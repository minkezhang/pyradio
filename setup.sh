#!/bin/bash

# for Ubuntu 12.10
# sudo apt-get -y install ffmpeg libavcodec-extra-53
# sudo apt-get -y install espeak

mkfifo stream

(python server.py > stream) &
# (python radio.py > stream) &
sleep 1;
mpg321 stream;
rm stream
./clean.sh
