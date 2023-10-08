docker stop dream-socket
docker rm dream-socket
docker image prune
docker build -t dream-socket:latest .
docker run -p 8070:8070 --restart unless-stopped -d --name dream-socket dream-socket:latest
