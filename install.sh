#!/bin/bash


if [ -z $(which ffmpeg) ]; then
  sudo add-apt-repository ppa:mc3man/trusty-media
  sudo add-apt-repository ppa:mc3man/gstffmpeg-keep
  sudo apt-get update -y
  sudo apt-get install ffmpeg gstreamer0.10-ffmpeg -y
fi
