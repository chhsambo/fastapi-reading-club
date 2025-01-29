# Building with FastAPI and Docker


## Docker Image

Build the docker image:
`$ docker build -t fastapi-reading-club .`

Run the docker image:
`$ docker run -p 80:80 fastapi-reading-club`


### WORKERS_PER_CORE
By default: **1**

`$ docker run -d -p 80:80 -e WORKERS_PER_CORE="3" fastapi-reading-club`
+ If you used the value 3 in a server with 2 CPU cores, it would run 6 worker processes.

for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have a FastAPI application that you know won't need high performance. And you don't want to waste server resources. You could make it use 0.5 workers per CPU core.

`$ docker run -d -p 80:80 -e WORKERS_PER_CORE="0.5" fastapi-reading-club`
+ In a server with 8 CPU cores, this would make it start only 4 worker processes.


### LOG_LEVEL

One of: debug, info, warning, error, critical
By default, set to **info**.

If you need to squeeze more performance sacrificing logging, set it to **warning**, for example:

`$ docker run -d -p 80:80 -e LOG_LEVEL="warning" fastapi-reading-club`


## Development live reload

For development, it's useful to be able to mount the contents of the application code inside of the container as a Docker "host volume", to be able to change the code and test it live, without having to build the image every time.

In that case, it's also useful to run the server with live auto-reload, so that it re-starts automatically at every code change.

**Usage**

For example, instead of running:
`$ docker run -d -p 80:80 fastapi-reading-club`

You could run:

`$ docker run -d -p 80:80 -v $(pwd):/code fastapi-reading-club`

`$ docker run --rm -p 8000:80 -v $(pwd)/app:/code/app fastapi-reading-club:python3.13`

`$ docker run --rm -p 8000:80 -v $(pwd)/app:/code/app -e LOG_LEVEL="warning" fastapi-reading-club:python3.13`

