docker build -t frontend .
docker tag frontend:latest sidvjsingh/frontend:1
docker push sidvjsingh/frontend:1