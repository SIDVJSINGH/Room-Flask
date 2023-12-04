FROM ubuntu:latest

LABEL authors="siddhant vijay singh"

RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Kolkata

RUN apt install -y wkhtmltopdf
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "./app.py"]
