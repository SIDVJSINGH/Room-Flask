FROM python:3-alpine3.15

LABEL authors="siddhant vijay singh"

RUN apk --no-cache add tzdata
ENV TZ=Asia/Kolkata

WORKDIR /applicaton

ADD . /applicaton

COPY . /applicaton

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python ./app.py
