#!/bin/env sh
cat /dev/urandom | head | sha1sum | cut -d " " -f 1 > /app/jwt.secret

export JWT_SECRET_KEY=b2d280fc0736e382f15edc563c641690963df889
export ADMIN_FLAG=CSCTF{0a97afb3-64be-4d96-aa52-86a91a2a3c52} 
export POST_FLAG=CSCTF{d2426fb5-a93a-4cf2-b353-eac8e0e9cf94} 
export SUPERADMIN_FLAG=CSCTF{759b2187-f746-49e1-90da-2b645d3cd61c} 
export REV_FLAG=CSCTF{5e18cbe9-7697-417a-9f6f-49dc30b0c660}
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=b3956724f51d9a64a37f83b2cedc1717df39d976
export POSTGRES_DB=production

uuid=$(cat /proc/sys/kernel/random/uuid)
user=$(cat /dev/urandom | head | md5sum | cut -d " " -f 1)
cat << EOF >> /docker-entrypoint-initdb.d/init.sql
	INSERT INTO users (username, password, role) VALUES ('superadmin', 'superadmin', 'superadmin');
    INSERT INTO posts (postid, username, title, data) VALUES ('$uuid', '$user', 'Welcome to the CTF!', '$ADMIN_FLAG');
EOF

docker-ensure-initdb.sh & 
GIN_MODE=release /app/chall & sleep 5
su postgres -c "postgres -D /var/lib/postgresql/data" &

nginx -g 'daemon off;' 