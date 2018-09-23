#!/bin/bash
cd video-gui
docker build --rm -f Dockerfile -t videos-gui .
cd ../video-service/videos_service
docker build --rm -f Dockerfile -t videos-service .
cd ../..
