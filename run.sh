docker pull realsleep/dream-socket:latest
docker stop dream-socket
docker rm dream-socket
docker run -p 8070:8070 --restart unless-stopped -d --name dream-socket realsleep/dream-socket:latest
