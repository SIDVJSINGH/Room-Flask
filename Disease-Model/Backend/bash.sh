# docker build -t backend .
# docker run -p 8000:8000 backend
docker tag backend:latest sidvjsingh/backend:1
docker push sidvjsingh/backend:1