FROM ubuntu:23.04 AS app

RUN apt-get update

WORKDIR /home/ctf

COPY run chall flag.txt ./

FROM redpwn/jail
COPY --from=app / /srv
COPY --from=app /dev /srv/dev
COPY --from=app /home/ctf/flag.txt /srv/app/flag.txt
COPY --from=app /home/ctf/run /srv/app/run
COPY --from=app /home/ctf/chall /srv/app/chall

RUN chmod +x /srv/app/run
RUN chmod +x /srv/app/chall

ENV JAIL_TIME=120
ENV JAIL_DEV=pts