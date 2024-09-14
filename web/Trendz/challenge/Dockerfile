FROM golang:alpine AS builder
RUN apk update && apk add --no-cache git binutils

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
ENV GIN_MODE=release
ENV PORT=8000
RUN go build -o /app/chall
RUN strip /app/chall

FROM postgres:alpine
RUN apk update && apk add --no-cache nginx
COPY nginx.conf /etc/nginx/nginx.conf

COPY run.sh /usr/local/bin/run.sh
COPY init.sql /docker-entrypoint-initdb.d/init.sql
WORKDIR /app
COPY --from=builder /app/chall /app/chall
COPY static static
COPY templates templates

ENTRYPOINT ["sh", "/usr/local/bin/run.sh"]