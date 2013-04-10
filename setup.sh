#!/bin/bash
mkfifo stream

(python radio.py > stream) &
sleep 1;
mpg321 stream;
rm stream
./clean.sh
