#!/usr/bin/sh

docker build --tag=syslooper .
docker run -p 5000:5000 --rm --privileged --name=syslooper -it syslooper