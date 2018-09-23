# Video silence remover 9001!
Hi, and welcome to the video silence remover 9001! (VSR) by Bruno Lopes

Email: brunoleonelopes@gmail.com

This readme tells you how to run the (VSR) and does a quick overview of what happens
behind the scenes.

This challenge was the development of a platform that removed silence scenes from mp4 videos.
This was a challenge undertaken by Bruno Lopes with the duration of 20h.

## Components
There are 3 main components.
->   GUI made with ReactJS and served with nginx. Available on localhost:80

->   Simple rest service written in python (flask(connexion), ffmpeg, videogrep, ) to do the conversion. You can see the endpoints by going to
	http://localhost:4001/v1/ui/

->   mongoDB database to store the metadata related with the videos



## Build images
If you have docker installed and can run it without admin permissions (sudo)
run

``` ./build_images.sh ```


## Run the images

with docker compose we can do

``` docker-compose up -d ```

to run the images and

``` docker-compose down ```

to shut things down

## Notes on further improving this tool
I'm available to talk about this work and explain my decisions, but if for some reason
it is not possible for you to reach me, you can read this section instead for things that i think can be improved.

This tool satisfies every requirement that was asked for the challenge
and does it with an high degree of elegance and simplicity.
Having said that I was only able to take the weekend to do this challenge. Because of that there are certain things that could be improved but didn't because of that time constraint.

First instead of using mondoDB to store the metadata of the videos a faster alternative would be
REDIS. I did not use it because the bottleneck is in the video proccess and using redis would make me take more time to study the python-redis interface.

For the video editing process, the celery lib would be a much more elegant alternative to run those long running
 tasks in the background (http://flask.pocoo.org/docs/0.12/patterns/celery/)
At the moment for each video conversion request we run a background daemon process.

After creating an array with noise timestamp intervals we use videogrep to take the video file
and create a new video with the timestamps given.
(https://github.com/antiboredom/videogrep)
Don't know if this tool is very efficient or stable.

We analyze each second to determine if its silent. If there is no sound that
reaches a certain threshold during each second, we classify it as silence.
We can improve this by using half second intervals instead and maybe tweaking with the threshold.

The GUI polls the back-end in regular intervals for updates on the conversion process. Instead of doing this, websockets would be more efficient.

If you reached the end of the readme file, congratulations for your endurance. Have a nice day!
